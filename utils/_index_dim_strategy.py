from typing import Callable

def _index_dim_strategy(
    args_schema: ArgsType,
    shard_row: Callable[[int], list[Placement | _ShardingPlaceholder]],
    partial_rules: list[list[Placement | _ShardingPlaceholder]] | None = None,
) -> list[list[Placement | _ShardingPlaceholder]]:
    """Common strategy for index ops that shard on all dims except the indexed dim.

    Args:
        shard_row: given a dim d, returns the strategy row for sharding on that dim.
        partial_rules: additional Partial passthrough strategies.
    """
    self_meta = cast(TensorMeta, args_schema[0])
    ndim = len(self_meta.shape)
    dim = normalize_dim(cast(int, args_schema[1]), ndim)
    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for d in range(ndim):
        if d != dim:
            strategies.append(shard_row(d))
    if partial_rules:
        strategies.extend(partial_rules)
    return strategies

