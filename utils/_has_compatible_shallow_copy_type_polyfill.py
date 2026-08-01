
def _has_compatible_shallow_copy_type_polyfill(
    input: torch.Tensor, from_: torch.Tensor
) -> bool:
    """
    Polyfill for torch._has_compatible_shallow_copy_type.

    Checks if two tensors have compatible types for shallow copying.
    The C++ implementation checks if input's TensorImpl has compatible shallow copy type
    with from_'s key_set. We approximate this by checking if both tensors are the same type.
    """
    # Check if both tensors are the same type (handles both regular tensors and subclasses)
    # This is more permissive than checking exact torch.Tensor type equality
    # but properly handles subclasses by allowing same-type shallow copies
    return type(input) is type(from_)

