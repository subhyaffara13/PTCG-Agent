
def is_ndonnx_namespace(xp: Namespace) -> bool:
    """
    Returns True if `xp` is an NDONNX namespace.

    See Also
    --------

    array_namespace
    is_numpy_namespace
    is_cupy_namespace
    is_torch_namespace
    is_dask_namespace
    is_jax_namespace
    is_pydata_sparse_namespace
    is_array_api_strict_namespace
    """
    return xp.__name__ == "ndonnx"

