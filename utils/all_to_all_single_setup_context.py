
def all_to_all_single_setup_context(ctx, inputs, output):
    """
    Setup context for all_to_all_single backward.

    Args:
        ctx: Context object to save state for backward
        inputs: Tuple of (input, output_split_sizes, input_split_sizes, group_name)
        output: Output from forward pass
    """
    input, output_split_sizes, input_split_sizes, group_name = inputs
    ctx.group_name = group_name
    ctx.output_split_sizes = output_split_sizes
    ctx.input_split_sizes = input_split_sizes

