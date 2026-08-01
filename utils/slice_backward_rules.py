
def slice_backward_rules(op_schema: OpSchema) -> OpStrategy:
    # func: slice_backward(Tensor grad_output, SymInt[] input_sizes, int dim, SymInt start, SymInt end, SymInt step) -> Tensor
    args_schema = op_schema.args_schema
    input_strategy, dim = args_schema[0], args_schema[2]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {input_strategy}")
    output_strategies: list[OpSpec] = []
    for placement_strategy in input_strategy.strategies:
        output_spec = placement_strategy.output_spec
        new_placements: list[Placement] = []
        for placement in output_spec.placements:
            # Redistribute to replicate only if the dim is sharded and matches the slice dim
            if _is_shard_like(placement) and placement.dim == dim:
                new_placements.append(Replicate())
            else:
                new_placements.append(placement)
        new_spec = DTensorSpec(output_spec.mesh, tuple(new_placements))
        redistribute_cost = [generate_redistribute_costs(input_strategy, new_spec)]
        new_strategy = OpSpec(
            output_specs=new_spec, redistribute_cost=redistribute_cost
        )
        output_strategies.append(new_strategy)
    return OpStrategy(output_strategies)

