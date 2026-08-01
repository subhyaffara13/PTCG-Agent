
def reduce_scatter_tensor_backward(ctx, grad_output: torch.Tensor):
    """
    Backward for reduce_scatter_tensor: all_gather.

    Forward reduces and scatters tensors to ranks, backward gathers gradients
    from all ranks.

    Args:
        ctx: Context object with group_name, group_size, and reduce_op
        grad_output: Gradient from downstream operations

    Returns:
        Tuple of (grad_input, grad_reduce_op, grad_group_size, grad_group_name)
        grad_reduce_op, grad_group_size, grad_group_name are None (not differentiable)
    """
    group_name = ctx.group_name
    group_size = ctx.group_size
    reduce_op = ctx.reduce_op

    # Lazy validation: check reduce_op only when backward is called
    if reduce_op != "sum":
        raise RuntimeError(
            f"reduce_scatter_tensor backward only supports 'sum' reduction, got '{reduce_op}'"
        )

    # Backward is all_gather
    output = torch.ops._c10d_functional.all_gather_into_tensor(
        grad_output.contiguous(),
        group_size,
        group_name,
    )
    return wait_tensor(output), None, None, None

