
def layer_norm_single_dim_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    input_meta = args_schema[0]
    normalized_shape = args_schema[1]
    weight_meta = args_schema[2]
    bias_meta = args_schema[3]

    axis = len(input_meta.shape) - len(normalize_to_torch_size(normalized_shape))

    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for dim in range(axis):
        # [out, mean, rstd, input, weight?, bias?]
        rule: list[Placement | _ShardingPlaceholder] = [
            _ShardingPlaceholder(dim),  # out
            _ShardingPlaceholder(dim),  # mean
            _ShardingPlaceholder(dim),  # rstd
            _ShardingPlaceholder(dim),  # input
        ]
        if weight_meta is not None:
            rule.append(Replicate())
        if bias_meta is not None:
            rule.append(Replicate())
        strategies.append(rule)
    return strategies

