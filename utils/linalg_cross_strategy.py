
def linalg_cross_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    ndim = _get_ndim(args_schema[0])
    cross_dim = kwargs_schema.get("dim", -1) % ndim
    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for dim in range(ndim):
        if dim == cross_dim:
            continue
        strategies.append([_ShardingPlaceholder(dim)] * 3)
    return strategies

