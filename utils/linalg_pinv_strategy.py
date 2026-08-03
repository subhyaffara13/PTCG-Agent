from typing import Any

def linalg_pinv_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    ndim = _get_ndim(args_schema[0])
    # Count optional tensor kwargs that are actually present
    extra_tensors = sum(
        isinstance(kwargs_schema.get(k), TensorMeta) for k in ("atol", "rtol")
    )
    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for dim in range(ndim - 2):
        s: list[Placement | _ShardingPlaceholder] = [
            _ShardingPlaceholder(dim),
            _ShardingPlaceholder(dim),
        ]
        # atol, rtol are scalar tensors — always Replicate
        s.extend([Replicate()] * extra_tensors)
        strategies.append(s)
    return strategies

