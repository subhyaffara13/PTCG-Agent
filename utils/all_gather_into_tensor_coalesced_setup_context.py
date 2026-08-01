
def all_gather_into_tensor_coalesced_setup_context(ctx, inputs, output):
    """
    Setup context for all_gather_into_tensor_coalesced backward.

    Args:
        ctx: Context object to save state for backward
        inputs: Tuple of (tensor_list, group_size, group_name)
        output: Output from forward pass
    """
    tensor_list, group_size, group_name = inputs
    ctx.group_name = group_name
    ctx.group_size = group_size

