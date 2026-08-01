
def select_backward_strategy(op_schema: OpSchema) -> OpStrategy:
    # func: select_backward(Tensor grad_output, SymInt[] input_sizes, int dim, SymInt index) -> Tensor
    args_schema = op_schema.args_schema
    input_strategy, dim = args_schema[0], args_schema[2]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {input_strategy}")
    if not isinstance(dim, int):
        raise AssertionError(f"Expected int, got {type(dim)}")
    output_strategies: list[OpSpec] = []
    for placement_strategy in input_strategy.strategies:
        input_spec = placement_strategy.output_spec
        # NOTE: shard_dim is guaranteed to exist because
        # grad_input has one more dim than grad_output
        output_placements = shift_shard_dims_after_insert(input_spec.placements, dim)
        output_specs = DTensorSpec(input_spec.mesh, tuple(output_placements))
        output_strategies.append(
            OpSpec(output_specs=output_specs, input_specs=(input_spec,))
        )
    return OpStrategy(output_strategies)

