
def sort_stable_strategy(op_schema: OpSchema) -> OpStrategy:
    # mostly copy paste from topk_strategy
    input_strategy = op_schema.args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")
    sort_dim = -1
    if "dim" in op_schema.kwargs_schema:
        sort_dim = cast(int, op_schema.kwargs_schema["dim"])
    return sort_strategy(op_schema, sort_dim)

