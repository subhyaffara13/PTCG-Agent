from typing import Callable

def _register_single_dim_pointwise(
    op: OpOverload,
    partial_extra_rules: list[list[Placement]] | None = None,
    static_argnum: int = 0,
) -> None:
    if partial_extra_rules is not None:
        _specially_registered_ops.add(op)
    inner_fn = _common_pointwise_single_dim_strategy(
        partial_extra_rules=partial_extra_rules  # pyrefly: ignore[bad-argument-type]
    )

    # Wrap to append tensor kwarg placements in schema declaration order.
    # out = output placement (s[0]); everything else (e.g. lr) = Replicate.
    # TODO: move kwargs handling upstream if this works
    def strategy_fn(
        op: OpOverload,
        args: ArgsType,
        kwargs: KwargsType,
        _fn: Callable = inner_fn,
    ) -> list[list[Placement | _ShardingPlaceholder]]:
        strategies = _fn(op, args, kwargs)
        kw_names = [k for k, v in kwargs.items() if isinstance(v, TensorMeta)]
        if not kw_names:
            return strategies
        return [
            s + [s[0] if name == "out" else Replicate() for name in kw_names]
            for s in strategies
        ]

    if _is_list_op(op):
        schema_info = RuntimeSchemaInfo(needs_pytree=True)
    else:
        schema_info = RuntimeSchemaInfo(static_argnum, static_kwargkey=["out"])
    # Fused ops (e.g. _fused_adam_) have state_steps on a potentially different
    # mesh; see the note in expand_to_full_mesh_op_strategy for details.
    different_mesh_args: list[int] | None = None
    if op.name().startswith("aten::_fused_"):
        different_mesh_args = [_FUSED_OP_SCALAR_IDX]
    register_single_dim_strategy(
        op,
        schema_info=schema_info,
        allow_uneven_sharding=True,
        allow_unbacked_sharding=True,
        different_mesh_args=different_mesh_args,
    )(strategy_fn)

