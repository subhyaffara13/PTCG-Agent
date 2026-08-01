
def all_to_all_single_backward(ctx, grad_output: torch.Tensor):
    """
    Backward for all_to_all_single: all_to_all with reversed split sizes.

    Forward does all-to-all with specified split sizes, backward reverses them.

    Args:
        ctx: Context object with group_name, output_split_sizes, and input_split_sizes
        grad_output: Gradient from downstream operations

    Returns:
        Tuple of (grad_input, grad_output_split_sizes, grad_input_split_sizes, grad_group_name)
        All except grad_input are None (not differentiable)
    """
    group_name = ctx.group_name
    output_split_sizes = ctx.output_split_sizes
    input_split_sizes = ctx.input_split_sizes

    # Backward is all_to_all with reversed split sizes
    output = torch.ops._c10d_functional.all_to_all_single(
        grad_output.contiguous(),
        input_split_sizes,  # Reversed
        output_split_sizes,  # Reversed
        group_name,
    )
    return wait_tensor(output), None, None, None

