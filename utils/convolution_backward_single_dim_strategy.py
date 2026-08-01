
def convolution_backward_single_dim_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder | None]]:
    bias_sizes = args_schema[3]
    has_bias = bias_sizes is not None
    # outputs: [grad_input, grad_weight, grad_bias]
    # inputs: [grad_output, input, weight]
    rule: list[Placement | _ShardingPlaceholder | None] = [
        _ShardingPlaceholder(0),  # grad_input
        Partial("sum"),  # grad_weight
        Partial("sum") if has_bias else None,  # grad_bias
        _ShardingPlaceholder(0),  # grad_output
        _ShardingPlaceholder(0),  # input
        Replicate(),  # weight
    ]
    return [rule]

