
def rms_norm_single_dim_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    input_meta = args_schema[0]
    normalized_shape = args_schema[1]
    weight_meta = args_schema[2]

    axis = len(input_meta.shape) - len(normalize_to_torch_size(normalized_shape))

    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for dim in range(axis):
        # [out, rrms, input, weight?]
        rule: list[Placement | _ShardingPlaceholder] = [
            _ShardingPlaceholder(dim),  # out
            _ShardingPlaceholder(dim),  # rrms
            _ShardingPlaceholder(dim),  # input
        ]
        if weight_meta is not None:
            rule.append(Replicate())
        strategies.append(rule)
    return strategies

