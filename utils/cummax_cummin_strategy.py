
def cummax_cummin_strategy(op_schema: OpSchema) -> OpStrategy:
    dim = cast(int, op_schema.args_schema[1])
    return sort_strategy(op_schema, dim)

