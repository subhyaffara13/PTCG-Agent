
def if_mask(mask: Any, val, *, _builder: object = None) -> tl.constexpr:
    """
    Work around triton compile error: `ValueError: `other` cannot be provided without `mask``
    A compile-time to check to return either `val` or `None` depending on the value of mask.
    """
    if isinstance(mask, tl.constexpr) and mask.value is None:
        return tl.constexpr(None)
    return val

