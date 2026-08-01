
def random_op_strategy(op_schema: OpSchema) -> StrategyType:
    self_strategy = op_schema.args_schema[0]
    if not isinstance(self_strategy, OpStrategy):
        raise AssertionError

    random_strategy = OpStrategy([])
    for arg_strategy in self_strategy.strategies:
        arg_spec = arg_strategy.output_spec
        if is_tensor_partial(arg_spec):
            # TODO: figure out how inplace random op should behave when it's partial
            raise RuntimeError(f"{op_schema.op} with Partial is not supported yet!")
        random_strategy.strategies.append(
            OpSpec(
                output_specs=arg_spec,
                input_specs=(arg_spec,),
                redistribute_cost=[[0.0] * len(self_strategy.strategies)],
            )
        )

    return random_strategy

