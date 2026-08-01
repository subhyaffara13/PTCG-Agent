
def is_dask_array(x: object) -> TypeIs[da.Array]:
    """
    Return True if `x` is a dask.array Array.

    This function does not import dask if it has not already been imported
    and is therefore cheap to use.

    See Also
    --------

    array_namespace
    is_array_api_obj
    is_numpy_array
    is_cupy_array
    is_torch_array
    is_ndonnx_array
    is_jax_array
    is_pydata_sparse_array
    """
    cls = cast(Hashable, type(x))
    return _issubclass_fast(cls, "dask.array", "Array")

