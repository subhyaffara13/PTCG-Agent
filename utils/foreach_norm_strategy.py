
def foreach_norm_strategy(op_schema: OpSchema) -> TupleStrategy:
    args_schema = op_schema.args_schema
    input_tuple_strategy = args_schema[0]
    if not isinstance(input_tuple_strategy, TupleStrategy):
        raise AssertionError(
            f"Expected TupleStrategy, got {type(input_tuple_strategy)}"
        )
    norm_type = args_schema[1] if len(args_schema) > 1 else 2
    if not isinstance(norm_type, (int, float, str)):
        raise AssertionError(f"Expected int, float, or str, got {type(norm_type)}")
    output_tuple_strategy_children: list[OpStrategy] = []
    for op_strategy in input_tuple_strategy.children:
        if not isinstance(op_strategy, OpStrategy):
            raise AssertionError(f"Expected OpStrategy, got {type(op_strategy)}")
        reduce_dims = list(range(op_strategy.ndim))
        output_strategy = common_reduction_strategy(
            op_strategy,
            reduce_dims,
            reduction_op=_get_norm_reduction_op(norm_type),
        )
        output_tuple_strategy_children.append(output_strategy)
    return TupleStrategy(output_tuple_strategy_children)

