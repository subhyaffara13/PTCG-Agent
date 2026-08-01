
def layer_norm_bwd_single_dim_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder | None]]:
    input_meta = args_schema[1]
    normalized_shape = args_schema[2]
    # mean = args_schema[3], rstd = args_schema[4]
    weight_meta = args_schema[5]
    bias_meta = args_schema[6]

    axis = len(input_meta.shape) - len(normalize_to_torch_size(normalized_shape))

    strategies: list[list[Placement | _ShardingPlaceholder | None]] = []
    for dim in range(axis):
        # outputs: [d_input, d_weight, d_bias] — always 3 per schema
        # d_weight/d_bias use None when weight/bias are None
        rule: list[Placement | _ShardingPlaceholder | None] = [
            _ShardingPlaceholder(dim),  # d_input
            Partial("sum") if weight_meta is not None else None,  # d_weight
            Partial("sum") if bias_meta is not None else None,  # d_bias
        ]
        # inputs: [grad_out, input, mean, rstd, weight?, bias?]
        rule.extend(
            [
                _ShardingPlaceholder(dim),  # grad_out
                _ShardingPlaceholder(dim),  # input
                _ShardingPlaceholder(dim),  # mean
                _ShardingPlaceholder(dim),  # rstd
            ]
        )
        if weight_meta is not None:
            rule.append(Replicate())
        if bias_meta is not None:
            rule.append(Replicate())
        strategies.append(rule)

    return strategies

