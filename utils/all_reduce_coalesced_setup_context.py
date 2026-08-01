
def all_reduce_coalesced_setup_context(ctx, inputs, output):
    """
    Setup context for all_reduce_coalesced backward.

    Args:
        ctx: Context object to save state for backward
        inputs: Tuple of (tensor_list, reduce_op, group_name)
        output: Output from forward pass
    """
    tensor_list, reduce_op, group_name = inputs
    ctx.group_name = group_name
    ctx.reduce_op = reduce_op.lower()

