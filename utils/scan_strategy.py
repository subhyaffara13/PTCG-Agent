
def scan_strategy(op_schema: OpSchema) -> OpStrategy:
    args_schema = op_schema.args_schema
    input_strategy = args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")
    dim = args_schema[1]
    if not isinstance(dim, int):
        raise AssertionError(f"Expected int, got {type(dim)}")
    return common_reduction_strategy(
        input_strategy, [dim], keep_dim=True, reduction_linear=False
    )

