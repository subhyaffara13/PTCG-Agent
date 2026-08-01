
def powsum_strategy(op_schema: OpSchema) -> OpStrategy:
    """
    Strategy for linalg__powsum: computes sum(|x|^ord) without the final root.
    Output is always reducible with Partial("sum").
    """
    args_schema = op_schema.args_schema
    input_strategy = args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")

    dim = args_schema[2] if len(args_schema) > 2 else None
    keepdim = args_schema[3] if len(args_schema) > 3 else False
    dims = _infer_reduction_dims(dim, input_strategy.ndim)
    reduce_dims = list(range(input_strategy.ndim)) if dims is None else dims
    return common_reduction_strategy(
        input_strategy,
        reduce_dims,
        keep_dim=cast(bool, keepdim),
        reduction_linear=True,
        reduction_op="sum",
    )

