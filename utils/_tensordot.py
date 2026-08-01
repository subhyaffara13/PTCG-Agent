
def _tensordot(x: ArrayType, y: ArrayType, axes: Tuple[int, ...], backend: str = "numpy") -> ArrayType:
    """Base tensordot."""
    fn = backends.get_func("tensordot", backend)
    return fn(x, y, axes=axes)

