
def gen_unbind_strategy(op_schema: OpSchema) -> StrategyType:
    """Forward all shardings except the unbind dimension."""
    input_strategy = op_schema.args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")
    input_ndim = input_strategy.ndim
    input_shape = input_strategy.shape
    unbind_dim = (
        cast(int, op_schema.args_schema[1]) if len(op_schema.args_schema) > 1 else 0
    )
    unbind_dim = normalize_dim(unbind_dim, input_ndim)

    mesh = input_strategy.mesh
    unbind_strategy = OpStrategy([])
    for arg_strategy in input_strategy.strategies:
        arg_spec = arg_strategy.output_spec
        if is_tensor_dim_sharded(arg_spec, dim=unbind_dim):
            raise RuntimeError(
                f"Attempted to unbind along the sharded dimension {unbind_dim}. ",
                "It cannot be performed without redistribution, which is disallowed "
                "by the current operator.",
            )
        # only add the strategy if the unbind dim is not sharded
        output_placements = shift_shard_dims_after_remove(
            arg_spec.placements, unbind_dim
        )
        output_specs = tuple(
            DTensorSpec(mesh, tuple(output_placements))
            for _ in range(input_shape[unbind_dim])
        )
        unbind_strategy.strategies.append(
            OpSpec(
                output_specs=output_specs,
                input_specs=(arg_spec,),
                redistribute_cost=[[0.0] * len(input_strategy.strategies)],
            )
        )
    return unbind_strategy

