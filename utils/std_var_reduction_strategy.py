
def std_var_reduction_strategy(op_schema: OpSchema) -> OpStrategy:
    args_schema = op_schema.args_schema
    input_strategy = args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")
    dims = None
    if len(op_schema.args_schema) > 1:
        dims = _infer_reduction_dims(args_schema[1], input_strategy.ndim)

    reduce_dims = list(range(input_strategy.ndim)) if dims is None else dims

    keep_dim = cast(bool, op_schema.kwargs_schema.get("keepdim", False))
    return common_reduction_strategy(
        input_strategy, reduce_dims, keep_dim=keep_dim, reduction_linear=False
    )

