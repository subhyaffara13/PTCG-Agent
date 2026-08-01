
def _wrap_tensor_autograd_backward(ctx, grad_output: torch.Tensor):
    """
    Backward for _wrap_tensor_autograd: identity (no-op).

    The wrapping is just for async optimization, gradients flow through unchanged.

    Args:
        ctx: Context object (unused)
        grad_output: Gradient from downstream operations

    Returns:
        Gradient unchanged (identity)
    """
    return grad_output

