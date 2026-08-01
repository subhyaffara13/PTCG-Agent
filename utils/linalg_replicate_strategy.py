
def linalg_replicate_strategy(op_schema: OpSchema) -> OpStrategy:
    """
    Since we do not have a simple way to compute some linear algebra operations
    like SVD or QR decomposition, always fall back to replicate.
    """
    args_schema = op_schema.args_schema
    input_strategy = args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")
    mesh = input_strategy.mesh

    output_strategies: list[OpSpec] = []
    for placement_strategy in input_strategy.strategies:
        replicate_placements = tuple(Replicate() for _ in range(mesh.ndim))
        replicate_spec = DTensorSpec(
            mesh=mesh,
            placements=replicate_placements,
            tensor_meta=placement_strategy.output_spec.tensor_meta,
        )
        redistribute_cost = [
            generate_redistribute_costs(input_strategy, replicate_spec)
        ]
        replicate_strategy = OpSpec(
            output_specs=replicate_spec,
            input_specs=(replicate_spec,),
            redistribute_cost=redistribute_cost,
        )
        output_strategies.append(replicate_strategy)
    return OpStrategy(output_strategies)

