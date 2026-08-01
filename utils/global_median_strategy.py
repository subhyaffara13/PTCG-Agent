
def global_median_strategy(op_schema: OpSchema) -> OpStrategy:
    input_strategy = cast(OpStrategy, op_schema.args_schema[0])
    reduce_dims = list(range(input_strategy.ndim))
    return common_reduction_strategy(
        input_strategy, reduce_dims, reduction_linear=False
    )

