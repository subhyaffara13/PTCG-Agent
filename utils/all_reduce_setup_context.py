
def all_reduce_setup_context(ctx, inputs, output):
    """
    Setup context for all_reduce backward.
    Args:
        ctx: Context object to save state for backward
        inputs: Tuple of (input, reduce_op, group_name)
        output: Output from forward pass
    """
    input, reduce_op, group_name = inputs
    ctx.group_name = group_name
    ctx.reduce_op = reduce_op.lower()

