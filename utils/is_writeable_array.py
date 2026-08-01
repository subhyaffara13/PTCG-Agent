
def is_writeable_array(x: object) -> TypeGuard[_ArrayApiObj]:
    """
    Return False if ``x.__setitem__`` is expected to raise; True otherwise.
    Return False if `x` is not an array API compatible object.

    Warning
    -------
    As there is no standard way to check if an array is writeable without actually
    writing to it, this function blindly returns True for all unknown array types.
    """
    cls = cast(Hashable, type(x))
    if _issubclass_fast(cls, "numpy", "ndarray"):
        return cast("npt.NDArray", x).flags.writeable
    res = _is_writeable_cls(cls)
    if res is not None:
        return res
    return hasattr(x, '__array_namespace__')

