
def grid_sampler_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    # grid_sampler_{2,3}d(input[N,C,...], grid[N,...,{2,3}]) -> output[N,C,...]
    # grid has no channel dim, so only batch sharding applies to both inputs.
    # Linear in input: P(sum/avg) on input with replicated grid is valid.
    return [
        [_ShardingPlaceholder(0)] * 3,
        [Partial("sum"), Partial("sum"), Replicate()],
        [Partial("avg"), Partial("avg"), Replicate()],
    ]

