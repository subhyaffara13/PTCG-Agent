
def sort_default_strategy(op_schema: OpSchema) -> OpStrategy:
    # mostly copy paste from topk_strategy
    input_strategy = op_schema.args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")
    sort_dim = -1
    if len(op_schema.args_schema) > 1:
        sort_dim = cast(int, op_schema.args_schema[1])
    return sort_strategy(op_schema, sort_dim)

