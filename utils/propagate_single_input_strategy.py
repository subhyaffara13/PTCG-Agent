
def propagate_single_input_strategy(op_schema: OpSchema) -> StrategyType:
    # For ops with a single tensor input, we perform a 1:1 mapping such that
    # for each strategy that the input supports, we create a corresponding strategy.
    # Note: this may be a complete waste of work, because it should be equivalent to
    # `return first_input_strategy` (unless creating a deep copy is important for some reason)
    if len([s for s in op_schema.args_schema if isinstance(s, OpStrategy)]) != 1:
        raise AssertionError(
            "propagate_single_input_strategy only works for single-tensor-input ops"
        )
    first_input_strategy = op_schema.args_schema[0]
    if not isinstance(first_input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(first_input_strategy)}")
    return OpStrategy(
        [
            OpSpec(
                output_specs=DTensorSpec(
                    mesh=first_input_strategy.mesh,
                    placements=strategy.output_spec.placements,
                    tensor_meta=strategy.output_spec.tensor_meta,
                ),
                input_specs=[
                    DTensorSpec(
                        mesh=first_input_strategy.mesh,
                        placements=strategy.output_spec.placements,
                        tensor_meta=strategy.output_spec.tensor_meta,
                    )
                ],
                redistribute_cost=[
                    generate_redistribute_costs(
                        first_input_strategy, strategy.output_spec
                    )
                ],
            )
            for strategy in first_input_strategy.strategies
        ]
    )

