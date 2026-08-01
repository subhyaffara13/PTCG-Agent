
def convolution_single_dim_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    bias_meta = args_schema[2]
    # [output, input, weight, (bias)]
    rule: list[Placement | _ShardingPlaceholder] = [
        _ShardingPlaceholder(0),  # output
        _ShardingPlaceholder(0),  # input
        Replicate(),  # weight
    ]
    if bias_meta is not None:
        rule.append(Replicate())  # bias
    return [rule]

