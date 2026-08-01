
def _is_writeable_cls(cls: type) -> bool | None:
    if (
        _issubclass_fast(cls, "numpy", "generic")
        or _issubclass_fast(cls, "jax", "Array")
        or _issubclass_fast(cls, "jax.core", "Tracer")  # see is_jax_array for limitations
        or _issubclass_fast(cls, "sparse", "SparseArray")
    ):
        return False
    if _is_array_api_cls(cls):
        return True
    return None

