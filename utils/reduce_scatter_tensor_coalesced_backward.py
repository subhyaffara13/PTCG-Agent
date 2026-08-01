
def reduce_scatter_tensor_coalesced_backward(ctx, grad_outputs: list[torch.Tensor]):
    """
    Backward for reduce_scatter_tensor_coalesced: all_gather each gradient.

    Forward reduces and scatters tensors to ranks, backward gathers gradients
    from all ranks.

    Args:
        ctx: Context object with group_name, group_size, and reduce_op
        grad_outputs: Gradients from downstream operations (one per input tensor)

    Returns:
        Tuple of (grad_inputs..., grad_reduce_op, grad_group_size, grad_group_name)
        grad_reduce_op, grad_group_size, grad_group_name are None (not differentiable)
    """
    group_name = ctx.group_name
    group_size = ctx.group_size
    reduce_op = ctx.reduce_op

    # Lazy validation: check reduce_op only when backward is called
    if reduce_op != "sum":
        raise RuntimeError(
            f"reduce_scatter_tensor_coalesced backward only supports 'sum' reduction, got '{reduce_op}'"
        )

    # Backward does all_gather on list of gradients
    grad_inputs = torch.ops._c10d_functional.all_gather_into_tensor_coalesced(
        [grad_output.contiguous() for grad_output in grad_outputs],
        group_size,
        group_name,
    )
    return (list(map(wait_tensor, grad_inputs)), None, None, None)

