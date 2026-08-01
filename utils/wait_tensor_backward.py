
def wait_tensor_backward(ctx, grad_output: torch.Tensor):
    """
    Backward for wait_tensor: identity (no-op).
    Wait is just a synchronization primitive, so gradient flows through unchanged.

    Args:
        ctx: Context object
        grad_output: Gradient from downstream operations

    Returns:
        Gradient unchanged (identity)
    """
    return grad_output

