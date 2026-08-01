
def all_gather_into_tensor_coalesced_backward(ctx, grad_outputs: list[torch.Tensor]):
    """
    Backward for all_gather_into_tensor_coalesced: reduce_scatter each gradient.

    Forward gathers tensors from all ranks, backward scatters gradients back
    with sum reduction.

    Args:
        ctx: Context object with group_name and group_size
        grad_outputs: Gradients from downstream operations (one per input tensor)

    Returns:
        Tuple of (grad_inputs..., grad_group_size, grad_group_name)
        grad_group_size and grad_group_name are None (not differentiable)
    """
    group_name = ctx.group_name
    group_size = ctx.group_size

    # Backward does reduce_scatter on list of gradients
    grad_inputs = torch.ops._c10d_functional.reduce_scatter_tensor_coalesced(
        [grad_output.contiguous() for grad_output in grad_outputs],
        "sum",
        group_size,
        group_name,
    )
    return (list(map(wait_tensor, grad_inputs)), None, None)

