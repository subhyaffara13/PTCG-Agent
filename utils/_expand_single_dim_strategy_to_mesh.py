
def _expand_single_dim_strategy_to_mesh(
    mesh: DeviceMesh,
    op_schema: OpSchema,
    strategy_info: _SingleDimStrategyInfo,
    output_tensor_meta: TensorMeta | Sequence[TensorMeta | None] | None,
) -> _ExpandedSingleDimStrategyFunc:
    """
    Expands the single_mesh_dim impl across all mesh dims, and expands ShardingPlacholder into all
    sharding types used by inputs.

    This supports functional correctness but will generate all possible combinations, which is prohibitively expensive
    for larger numbers of mesh dimensions.

    The expanded_strategy function accesses both the args_schema/kwargs_schema, which contains TensorMeta in place of
    tensor arguments, but also the op_schema which contains OpStrategy in place of Tensor args.

    Args:
        output_tensor_meta: tensor metadata for the output(s), precomputed during sharding prop
    """
    # Note: circular import, failed to untangle with #168221, reverted
    from torch.distributed.tensor._ops.utils import expand_to_full_mesh_op_strategy

    def _create_expanded_strategy_impl(
        op_schema: OpSchema,
        output_tensor_meta: TensorMeta | Sequence[TensorMeta | None] | None,
    ) -> Callable[[OpOverload, ArgsType, KwargsType], StrategyType]:
        def expanded_strategy(
            op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
        ) -> StrategyType:
            prepared_strategy = _PreparedSingleDimStrategy(
                strategy_info, op_schema, output_tensor_meta
            )

            # Detect inplace ops by checking if the base op name ends with '_'
            op_name = op.name()
            base_name = op_name.split("::")[1].split(".")[0]
            is_inplace = base_name.endswith("_")

            element_mesh = prepared_strategy.element_mesh or mesh

            return expand_to_full_mesh_op_strategy(
                element_mesh,
                op_schema,
                prepared_strategy.expanded_strategies,
                output_tensor_meta=output_tensor_meta,
                inplace_op=is_inplace,
                input_index=prepared_strategy.num_outputs,
                allow_unbacked_sharding=prepared_strategy.allow_unbacked_sharding,
                allow_uneven_sharding=prepared_strategy.allow_uneven_sharding,
                different_mesh_args=prepared_strategy.remapped_different_mesh_args,
            )

        return expanded_strategy

    # Create a cached version of the impl
    _cached_create_expanded_strategy = functools.lru_cache(
        _create_expanded_strategy_impl
    )

    def _create_expanded_strategy(
        op_schema: OpSchema,
        output_tensor_meta: TensorMeta | Sequence[TensorMeta | None] | None,
    ) -> Callable[[OpOverload, ArgsType, KwargsType], StrategyType]:
        # Try to use cache, but fall back to uncached version if hashing fails
        # (e.g., when TensorMeta contains SymInts from dynamic shapes)
        try:
            return _cached_create_expanded_strategy(op_schema, output_tensor_meta)
        except TypeError:
            # Unhashable types (SymInts), skip caching
            return _create_expanded_strategy_impl(op_schema, output_tensor_meta)

    def _translate_list_op_schema(
        op_schema: OpSchema,
        output_tensor_meta: Sequence[TensorMeta] | None,
        index: int,
    ) -> tuple[OpSchema, TensorMeta | None]:
        """Translate foreach/fused op to per-element version of schema."""
        op_parts = str(op_schema.op).split(".")
        op_name = op_parts[-2]
        foreach_variant = op_parts[-1]

        # select per-element inputs, outputs
        target_args, target_kwargs = tree_map_only(
            TupleStrategy,
            lambda x: x.children[index],
            (op_schema.args_schema, op_schema.kwargs_schema),
            is_leaf=lambda x: isinstance(x, TupleStrategy),
        )
        # For inplace ops, output_tensor_meta is None
        target_output_meta = (
            output_tensor_meta[index] if output_tensor_meta is not None else None
        )

        # Strip the prefix to get the base op name and find the per-element op.
        # Fused ops (e.g. _fused_adam) have no per-element ATen equivalent,
        # so we keep the original op unchanged.
        if op_name.startswith("_foreach_"):
            base_op_name = op_name.replace("_foreach_", "", 1)
        elif op_name.startswith("_amp_foreach_"):
            base_op_name = op_name.replace("_amp_foreach_", "", 1)
        else:
            # Fused ops or unknown: keep original op, no translation
            target_op = op_schema.op
            op_schema = OpSchema(
                target_op,  # type: ignore[arg-type]
                args_schema=tuple(target_args),
                kwargs_schema=op_schema.kwargs_schema,
            )
            return op_schema, target_output_meta

        # Strip trailing underscore for inplace ops
        base_op_name = base_op_name.removesuffix("_")

        # figure out target op variant
        variant_map = {
            "List": "Tensor",
            "ScalarList": "Scalar",
            "Scalar": "Scalar",
            "Tensor": "Tensor",
            "default": "default",
        }
        target_variant = (
            "default"
            if len(target_args) == 1
            else variant_map.get(foreach_variant, "default")
        )

        # this seems a bit messy
        base_op = getattr(torch.ops.aten, base_op_name)
        target_op = (
            getattr(base_op, target_variant)
            if target_variant in base_op.overloads()
            else base_op.default
        )

        op_schema = OpSchema(
            target_op,  # type: ignore[arg-type]
            args_schema=tuple(target_args),
            kwargs_schema=op_schema.kwargs_schema,
        )
        return op_schema, target_output_meta

    def expanded_foreach_strategy(
        op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
    ) -> StrategyType:
        tensorlist_len: int | None = None
        for i, obj in enumerate(op_schema.args_schema):
            if isinstance(obj, TupleStrategy):
                if tensorlist_len is None:
                    tensorlist_len = len(obj.children)
                elif len(obj.children) != tensorlist_len:
                    raise AssertionError(
                        f"Expected {tensorlist_len} children in index {i}, but found {len(obj.children)}."
                    )

        if tensorlist_len is None:
            raise AssertionError("Must have at least one tuple input to a foreach op")

        child_strategies: list[StrategyType] = []
        for tensorlist_i in range(tensorlist_len):
            per_index_schema, per_index_output_meta = _translate_list_op_schema(
                op_schema,
                output_tensor_meta,  # type: ignore[arg-type]
                tensorlist_i,
            )
            per_index_strategy = _create_expanded_strategy(
                per_index_schema, per_index_output_meta
            )
            child_strategies.append(
                per_index_strategy(
                    op, per_index_schema.args_meta, per_index_schema.kwargs_meta
                )
            )

        return TupleStrategy(children=child_strategies)

    # TODO maybe this could be helped by adding a new 'tag' to the OpOverload?
    # Only use the foreach path if the op has TupleStrategy inputs (i.e., actual
    # list-of-tensor args). The name prefix alone is insufficient because ops like
    # _fused_rms_norm share the "_fused_" prefix but are not foreach/fused-optimizer ops.
    op_name = op_schema.op.name()
    has_tuple_strategy = any(
        isinstance(arg, TupleStrategy) for arg in op_schema.args_schema
    )
    if has_tuple_strategy and op_name.startswith(
        ("aten::_foreach_", "aten::_amp_foreach_", "aten::_fused_")
    ):
        return expanded_foreach_strategy

    return _create_expanded_strategy(op_schema, output_tensor_meta)

