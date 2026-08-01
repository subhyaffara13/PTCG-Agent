
def argmax_argmin_strategy(op_schema: OpSchema) -> OpStrategy:
    """
    Strategy for argmax/argmin. These return indices, not values, so they cannot
    use P(max/min) output placements. The indices are local to each shard and
    cannot be meaningfully combined across ranks with a max/min reduction.
    Force redistribution on reduction dimensions by using reduction_linear=False.
    """
    args_schema = op_schema.args_schema
    input_strategy = args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")

    dims = None
    if len(op_schema.args_schema) > 1:
        dims = _infer_reduction_dims(args_schema[1], input_strategy.ndim)

    reduce_dims = list(range(input_strategy.ndim)) if dims is None else dims
    keep_dim = len(op_schema.args_schema) > 2 and bool(op_schema.args_schema[2])
    reduction_op = ARGMAX_ARGMIN_OPS[op_schema.op]
    return common_reduction_strategy(
        input_strategy,
        reduce_dims,
        keep_dim=keep_dim,
        reduction_linear=False,  # Force redistribution - indices can't use P(max/min)
        # reduction_op is effectively unused here: reduction_linear=False
        # forces all reduction-dim Shard placements to Replicate before
        # map_placements_after_reduction, so no Shard-on-reduction-dim
        # remains to convert to Partial. Passed for consistency.
        reduction_op=reduction_op,
    )

