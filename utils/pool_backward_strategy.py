
def pool_backward_strategy(
    op: torch._ops.OpOverload,
    args_schema: tuple[Any, ...],
    kwargs_schema: dict[str, Any],
) -> list[list[Placement | _ShardingPlaceholder]]:
    # max_pool2d_with_indices_backward(grad_output, self, ..., indices) -> grad_input
    # 1 output + 3 tensor inputs = 4 placements
    # Order: [output, grad_output, self, indices]
    input_meta = cast(TensorMeta, args_schema[0])
    strategies: list[list[Placement | _ShardingPlaceholder]] = [
        [_ShardingPlaceholder(0)] * 4,
    ]
    if len(input_meta.shape) >= 4:  # batched: (N, C, H, W)
        strategies.append([_ShardingPlaceholder(1)] * 4)
    # The backward is linear in grad_output, so P(sum/avg) pass through.
    # indices must be replicated (integer positions, not reducible).
    # self is only used for shape, so replicate it too.
    r = Replicate()
    for reduce_op in ("sum", "avg"):
        p = Partial(reduce_op)
        strategies.append([p, p, r, r])
    return strategies

