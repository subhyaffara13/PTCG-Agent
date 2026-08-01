
def softmax_strategy(op_schema: OpSchema) -> OpStrategy:
    input_strategy, softmax_dim, *_ = op_schema.args_schema
    input_strategy = cast(OpStrategy, input_strategy)

    softmax_dim = cast(int, softmax_dim)
    softmax_dim = normalize_dim(softmax_dim, input_strategy.ndim)

    output_strategy = OpStrategy([])
    for input_placement_strategy in input_strategy.strategies:
        redistribute_costs = []
        input_src_spec = input_placement_strategy.output_spec

        # make sure input is replicated along the softmax dim
        input_target_spec = DTensorSpec(
            mesh=input_strategy.mesh,
            placements=replicate_reduction_dims(
                input_src_spec.placements, [softmax_dim]
            ),
            tensor_meta=input_src_spec.tensor_meta,
        )
        redistribute_costs.append(
            generate_redistribute_costs(input_strategy, input_target_spec)
        )
        output_target_spec = input_target_spec
        output_strategy.strategies.append(
            OpSpec(
                output_specs=output_target_spec,
                input_specs=[input_target_spec],
                redistribute_cost=redistribute_costs,
            )
        )

    return output_strategy

