
def is_cupy_array(x: object) -> bool:
    """
    Return True if `x` is a CuPy array.

    This function does not import CuPy if it has not already been imported
    and is therefore cheap to use.

    This also returns True for `cupy.ndarray` subclasses and CuPy scalar objects.

    See Also
    --------

    array_namespace
    is_array_api_obj
    is_numpy_array
    is_torch_array
    is_ndonnx_array
    is_dask_array
    is_jax_array
    is_pydata_sparse_array
    """
    cls = cast(Hashable, type(x))
    return _issubclass_fast(cls, "cupy", "ndarray")

