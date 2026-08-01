
def is_jax_namespace(xp: Namespace) -> bool:
    """
    Returns True if `xp` is a JAX namespace.

    This includes ``jax.numpy`` and ``jax.experimental.array_api`` which existed in
    older versions of JAX.

    See Also
    --------

    array_namespace
    is_numpy_namespace
    is_cupy_namespace
    is_torch_namespace
    is_ndonnx_namespace
    is_dask_namespace
    is_pydata_sparse_namespace
    is_array_api_strict_namespace
    """
    return xp.__name__ in {"jax.numpy", "jax.experimental.array_api"}

