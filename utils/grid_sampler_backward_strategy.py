from typing import Any

def grid_sampler_backward_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    # grid_sampler_{2,3}d_backward: 2 outputs (grad_input, grad_grid) + 3 inputs = 5 placements, batch-only
    return [[_ShardingPlaceholder(0)] * 5]

