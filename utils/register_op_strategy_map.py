
def register_op_strategy_map(
    aten_op_overload: torch._ops.OpOverload,
    local_op_name: Callable[..., torch.Tensor],
    schema_info: RuntimeSchemaInfo | None = None,
    strict_view: bool = False,
) -> None:
    """
    Helper that registers strategies for view-like operators that follow a pattern:
      (1) define the way input dims are split/combined to form output dims (dim_maps)
      (2) register a strategy for the op schema that uses the dim_map as a sharding prop rule

    strict_view: if True, we will error out if the view-operation would require resharding the input.
       Currently, this should be set to 'true' for any "view" ops.
       We could diverge behavior for "reshape" ops which could perform a redistribute implicitly.
    """
    dim_map: Callable[..., DimMap] = dim_maps[local_op_name]

    @register_op_strategy(aten_op_overload, schema_info=schema_info)
    def reshape_strategy(op_schema: OpSchema) -> StrategyType:
        rules = dim_map(*op_schema.args_schema, **op_schema.kwargs_schema)
        input_strategy = cast(OpStrategy, op_schema.args_schema[0])
        mesh = op_schema.get_mesh_from_args(validate=False)

        global_in_shape = input_strategy.shape
        if global_in_shape is None:
            raise AssertionError("Shape required.")

        output_strategy = OpStrategy([])
        for input_placement_strategy in input_strategy.strategies:
            input_src_spec = input_placement_strategy.output_spec

            input_tgt_placements, output_placements = propagate_shape_and_sharding(
                input_src_spec.placements,
                tuple(global_in_shape),
                rules,
                mesh.shape,
                strict_view,
            )

            # TODO: optimize this. we shouldn't simply blindly replicate
            #       unshardable dims ...
            # FIXME: this can be wrong for situations where we have
            #        [Shard(0), Shard(0)]
            input_tgt_spec = DTensorSpec(
                placements=tuple(input_tgt_placements),
                mesh=mesh,
                tensor_meta=input_src_spec.tensor_meta,
                use_strided_shard_as_shard_order=False,
            )
            redistribute_costs: list[list[float]] = [
                generate_redistribute_costs(input_strategy, input_tgt_spec)
            ]

            output_spec = DTensorSpec(
                mesh=mesh,
                placements=tuple(output_placements),
                use_strided_shard_as_shard_order=False,
            )
            output_strategy.strategies.append(
                OpSpec(
                    output_specs=output_spec,
                    input_specs=(input_tgt_spec,),
                    redistribute_cost=redistribute_costs,
                )
            )

        return output_strategy

