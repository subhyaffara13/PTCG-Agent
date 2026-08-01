
def debug_unwrap(tensor: torch.Tensor, *, recurse: bool = True) -> torch.Tensor:
    """Unwraps a functorch tensor (e.g. BatchedTensor, GradTrackingTensor) to its underlying tensor.

    This function should only be used in a debug setting (e.g. trying to print the
    value of a Tensor in a debugger). Otherwise, using the result of function
    inside of a function being transformed will lead to undefined behavior.
    """
    if not is_functorch_wrapped_tensor(tensor):
        return tensor
    result = get_unwrapped(tensor)
    if recurse:
        return debug_unwrap(result)
    return result

