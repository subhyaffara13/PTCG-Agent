
def reduce_scatter_tensor_setup_context(ctx, inputs, output):
    """
    Setup context for reduce_scatter_tensor backward.

    Args:
        ctx: Context object to save state for backward
        inputs: Tuple of (input, reduce_op, group_size, group_name)
        output: Output from forward pass
    """
    input, reduce_op, group_size, group_name = inputs
    ctx.group_name = group_name
    ctx.group_size = group_size
    ctx.reduce_op = reduce_op.lower()

