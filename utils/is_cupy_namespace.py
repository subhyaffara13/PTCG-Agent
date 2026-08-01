
def is_cupy_namespace(xp: Namespace) -> bool:
    """
    Returns True if `xp` is a CuPy namespace.

    This includes both CuPy itself and the version wrapped by array-api-compat.

    See Also
    --------

    array_namespace
    is_numpy_namespace
    is_torch_namespace
    is_ndonnx_namespace
    is_dask_namespace
    is_jax_namespace
    is_pydata_sparse_namespace
    is_array_api_strict_namespace
    """
    return xp.__name__ in {"cupy", _compat_module_name() + ".cupy"}

