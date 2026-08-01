
def foreach_powsum_strategy(op_schema: OpSchema) -> TupleStrategy:
    """
    Strategy for _foreach_powsum: computes sum(|x|^ord) for each tensor.
    Output is always reducible with Partial("sum").
    """
    args_schema = op_schema.args_schema
    input_tuple_strategy = args_schema[0]
    if not isinstance(input_tuple_strategy, TupleStrategy):
        raise AssertionError(
            f"Expected TupleStrategy, got {type(input_tuple_strategy)}"
        )
    output_tuple_strategy_children: list[OpStrategy] = []
    for op_strategy in input_tuple_strategy.children:
        if not isinstance(op_strategy, OpStrategy):
            raise AssertionError(f"Expected OpStrategy, got {type(op_strategy)}")
        reduce_dims = list(range(op_strategy.ndim))
        output_strategy = common_reduction_strategy(
            op_strategy,
            reduce_dims,
            reduction_linear=True,
            reduction_op="sum",
        )
        output_tuple_strategy_children.append(output_strategy)
    return TupleStrategy(output_tuple_strategy_children)

