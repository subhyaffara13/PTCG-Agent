
def create_like_strategy(op_schema: OpSchema) -> StrategyType:
    # create_like_strategy deals with ops that creating tensors with same
    # shape as input, but with specific content that does not depend on
    # the input, we can propagate sharding, but we have to make sure we
    # move from partial to replicated.
    select_strategy = op_schema.args_schema[0]
    create_like_strategy = OpStrategy([])
    if not isinstance(select_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(select_strategy)}")
    for arg_strategy in select_strategy.strategies:
        arg_spec = arg_strategy.output_spec
        output_spec = DTensorSpec(
            mesh=select_strategy.mesh,
            placements=tuple(
                Replicate() if isinstance(p, Partial) else p
                for p in arg_spec.placements
            ),
            tensor_meta=arg_spec.tensor_meta,
        )
        create_like_strategy.strategies.append(
            OpSpec(
                output_specs=output_spec,
                input_specs=(arg_spec,),
                redistribute_cost=[
                    generate_redistribute_costs(select_strategy, arg_spec),
                ],
            )
        )

    return create_like_strategy

