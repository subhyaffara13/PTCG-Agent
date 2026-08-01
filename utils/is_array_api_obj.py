
def is_array_api_obj(x: object) -> TypeGuard[_ArrayApiObj]:
    """
    Return True if `x` is an array API compatible array object.

    See Also
    --------

    array_namespace
    is_numpy_array
    is_cupy_array
    is_torch_array
    is_ndonnx_array
    is_dask_array
    is_jax_array
    """
    return (
        hasattr(x, '__array_namespace__') 
        or _is_array_api_cls(cast(Hashable, type(x)))
    )

