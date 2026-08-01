
def transpose_strategy(op_schema: OpSchema) -> OpStrategy:
    self_strategy = op_schema.args_schema[0]
    if not isinstance(self_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(self_strategy)}")

    transpose_strategies = []
    for input_strategy in self_strategy.strategies:
        input_spec = input_strategy.output_spec
        ndim = input_spec.ndim
        # t() on 1D tensor is a no-op, preserve placements
        # t() on 2D tensor swaps dims 0 and 1
        if ndim <= 1:
            output_placements = list(input_spec.placements)
        else:
            output_placements: list[Placement] = []
            for p in input_spec.placements:
                if isinstance(p, _StridedShard):
                    output_placements.append(
                        _StridedShard(1 - p.dim, split_factor=p.split_factor)
                    )
                elif isinstance(p, Shard):
                    output_placements.append(Shard(1 - p.dim))
                else:
                    output_placements.append(p)
        transpose_strategy = OpSpec(
            output_specs=DTensorSpec(
                mesh=input_strategy.mesh,
                placements=tuple(output_placements),
            ),
            input_specs=(input_strategy.output_spec,),
        )
        transpose_strategies.append(transpose_strategy)

    return OpStrategy(strategies=transpose_strategies)

