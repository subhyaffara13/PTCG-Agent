
def _has_dtensor_support(aten_op: OpOverload) -> bool:
    """Check if an aten op has any DTensor sharding strategy registered."""
    propagator = DTensor._op_dispatcher.sharding_propagator
    if aten_op in propagator.op_single_dim_strategy_funcs:
        return True
    if aten_op in propagator.op_strategy_funcs:
        return True
    return DecompShardingStrategy.has_decomp(aten_op)

