
def _linalg_batch_dim_strategies(
    ndim: int, n_placements: int
) -> list[list[Placement | _ShardingPlaceholder]]:
    """Build single-dim strategies for linalg ops that operate on the last 1-2 dims.

    Returns sharding on each batch dim (all dims except the last 2), with all
    outputs and inputs sharded on the same dim.
    """
    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for dim in range(ndim - 2):
        strategies.append([_ShardingPlaceholder(dim)] * n_placements)
    return strategies

