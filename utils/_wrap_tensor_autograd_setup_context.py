
def _wrap_tensor_autograd_setup_context(ctx, inputs, output):
    """
    Setup context for _wrap_tensor_autograd backward.

    Args:
        ctx: Context object to save state for backward (nothing to save)
        inputs: Tuple of (input,)
        output: Output from forward pass
    """
    return

