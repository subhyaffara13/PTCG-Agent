
def interp_pool_1out_2in_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    # 1 output + 2 inputs = 3 placements; shard on batch (0) and channel (1)
    return [
        [_ShardingPlaceholder(0)] * 3,
        [_ShardingPlaceholder(1)] * 3,
    ]

