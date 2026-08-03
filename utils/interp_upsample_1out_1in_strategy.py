from typing import Any

def interp_upsample_1out_1in_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    # 1 output + 1 input = 2 placements; shard on batch (0) and channel (1)
    # Upsample is a linear transformation so Partial(sum/avg) is valid.
    return [
        [_ShardingPlaceholder(0)] * 2,
        [_ShardingPlaceholder(1)] * 2,
        [Partial("sum"), Partial("sum")],
        [Partial("avg"), Partial("avg")],
    ]

