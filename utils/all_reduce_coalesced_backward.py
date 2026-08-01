
def all_reduce_coalesced_backward(ctx, grad_outputs: list[torch.Tensor]):
    """
    Backward for all_reduce_coalesced: all_reduce each gradient.

    Forward aggregates tensors, backward aggregates gradients.

    Args:
        ctx: Context object with group_name and reduce_op
        grad_outputs: Gradients from downstream operations (one per input tensor)

    Returns:
        Tuple of (grad_inputs..., grad_reduce_op, grad_group_name)
        grad_reduce_op and grad_group_name are None (not differentiable)
    """
    group_name = ctx.group_name
    reduce_op = ctx.reduce_op

    if reduce_op != "sum":
        raise RuntimeError(
            f"all_reduce_coalesced backward only supports 'sum' reduction, got '{reduce_op}'"
        )

    # Backward does all_reduce on list of gradients
    grad_inputs = torch.ops._c10d_functional.all_reduce_coalesced(
        [grad_output.contiguous() for grad_output in grad_outputs],
        reduce_op,
        group_name,
    )
    return (list(map(wait_tensor, grad_inputs)), None, None)

