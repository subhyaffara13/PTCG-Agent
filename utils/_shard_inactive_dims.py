
def _shard_inactive_dims(
    ndim: int, active_dims: set[int], num_inputs: int = 1
) -> list[list[Placement | _ShardingPlaceholder]]:
    """Single-dim strategies: shard on dims the op doesn't touch."""
    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for d in range(ndim):
        if d not in active_dims:
            strategies.append([_ShardingPlaceholder(d)] * (1 + num_inputs))
    return strategies

