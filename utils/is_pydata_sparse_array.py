
def is_pydata_sparse_array(x: object) -> TypeIs[sparse.SparseArray]:
    """
    Return True if `x` is an array from the `sparse` package.

    This function does not import `sparse` if it has not already been imported
    and is therefore cheap to use.


    See Also
    --------

    array_namespace
    is_array_api_obj
    is_numpy_array
    is_cupy_array
    is_torch_array
    is_ndonnx_array
    is_dask_array
    is_jax_array
    """
    # TODO: Account for other backends.
    cls = cast(Hashable, type(x))
    return _issubclass_fast(cls, "sparse", "SparseArray")

