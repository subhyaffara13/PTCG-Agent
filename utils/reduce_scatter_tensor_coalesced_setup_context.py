
def reduce_scatter_tensor_coalesced_setup_context(ctx, inputs, output):
    """
    Setup context for reduce_scatter_tensor_coalesced backward.

    Args:
        ctx: Context object to save state for backward
        inputs: Tuple of (tensor_list, reduce_op, group_size, group_name)
        output: Output from forward pass
    """
    tensor_list, reduce_op, group_size, group_name = inputs
    ctx.group_name = group_name
    ctx.group_size = group_size
    ctx.reduce_op = reduce_op.lower()

