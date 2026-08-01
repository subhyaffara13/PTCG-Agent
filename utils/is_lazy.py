
def is_lazy(param: Any) -> bool:
    """
    Returns whether ``param`` is an ``UninitializedParameter`` or ``UninitializedBuffer``.

    Args:
        param (Any): the input to check.
    """
    return isinstance(param, UninitializedTensorMixin)

