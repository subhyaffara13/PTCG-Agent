
def new_factory_strategy(op_schema: OpSchema) -> StrategyType:
    # Currently there are two strategies:
    # 1. let the output be replicated
    # 2. let the output follow the input if input and output have the same shape
    input_strategy = op_schema.args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")

    mesh = input_strategy.mesh
    input_shape = input_strategy.shape
    output_shape = op_schema.args_schema[1]
    if not isinstance(output_shape, list):
        raise AssertionError(f"Expected list, got {type(output_shape)}")

    new_factory_strategy = OpStrategy([])
    for arg_strategy in input_strategy.strategies:
        input_spec = arg_strategy.output_spec
        replica_spec = DTensorSpec(mesh, tuple([Replicate()] * mesh.ndim))
        new_factory_strategy.strategies.append(
            OpSpec(
                output_specs=replica_spec,
                input_specs=(input_spec,),
                redistribute_cost=[[0.0] * len(input_strategy.strategies)],
            )
        )

        if tuple(input_shape) == tuple(output_shape) and input_spec.is_sharded():
            new_factory_strategy.strategies.append(
                OpSpec(
                    output_specs=input_spec,
                    input_specs=(input_spec,),
                    # encouraging new tensor placement to be the same as input
                    redistribute_cost=[[-0.1] * len(input_strategy.strategies)],
                )
            )

    return new_factory_strategy

