
def topk_strategy(op_schema: OpSchema) -> OpStrategy:
    topk_dim = (
        cast(int, op_schema.args_schema[2]) if len(op_schema.args_schema) > 2 else -1
    )
    return sort_strategy(op_schema, topk_dim)

