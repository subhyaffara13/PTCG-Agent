
def all_gather_into_tensor_backward(ctx, grad_output: torch.Tensor):
    """
    Backward for all_gather_into_tensor: reduce_scatter with sum.

    Forward gathers tensors from all ranks, backward scatters gradients back
    with sum reduction.

    Args:
        ctx: Context object with group_name and group_size
        grad_output: Gradient from downstream operations

    Returns:
        Tuple of (grad_input, grad_group_size, grad_group_name)
        grad_group_size and grad_group_name are None (not differentiable)
    """
    group_name = ctx.group_name
    group_size = ctx.group_size

    # Backward is reduce_scatter with sum
    output = torch.ops._c10d_functional.reduce_scatter_tensor(
        grad_output.contiguous(),
        "sum",
        group_size,
        group_name,
    )
    return wait_tensor(output), None, None

