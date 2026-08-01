
def _wrap_tensor_autograd(input: torch.Tensor) -> torch.Tensor:
    """
    Custom op that allows autograd to propagate
    from a normal Tensor to an AsyncCollectiveTensor.

    This is the low-level implementation. Users should call _maybe_wrap_tensor directly.

    Args:
        input: Input tensor to wrap in AsyncCollectiveTensor

    Returns:
        AsyncCollectiveTensor wrapping the input (or wait_tensor result if tracing)
    """
    return AsyncCollectiveTensor(input)

