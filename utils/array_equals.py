
def array_equals(left: ArrayLike, right: ArrayLike) -> bool:
    """
    ExtensionArray-compatible implementation of array_equivalent.
    """
    if left.dtype != right.dtype:
        return False
    elif isinstance(left, ABCExtensionArray):
        return left.equals(right)
    else:
        return array_equivalent(left, right, dtype_equal=True)

