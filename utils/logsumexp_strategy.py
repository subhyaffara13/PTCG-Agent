
def logsumexp_strategy(op_schema: OpSchema) -> OpStrategy:
    """Implements the sharding propagation strategy for logsumexp."""

    # args_schema contains all but the DTensor args (e.g., dim, keepdim).
    args_schema = op_schema.args_schema
    if not len(args_schema) > 1:
        raise AssertionError(
            f"Expected more than 1 arg (input and dim are required), got {len(args_schema)}"
        )

    input_strategy = args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")

    dims_arg = args_schema[1]
    reduce_dims = _infer_reduction_dims(dims_arg, input_strategy.ndim)
    if reduce_dims is None:
        raise AssertionError("Expected reduce_dims to not be None")

    keep_dim = cast(bool, op_schema.kwargs_schema.get("keepdim", False))
    return common_reduction_strategy(
        input_strategy,
        reduce_dims,
        keep_dim=keep_dim,
        reduction_linear=False,
    )

