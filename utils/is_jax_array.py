
def is_jax_array(x: object) -> TypeIs[jax.Array]:
    """
    Return True if `x` is a JAX array.

    This function does not import JAX if it has not already been imported
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
    is_pydata_sparse_array
    """
    cls = cast(Hashable, type(x))
    # We test for jax.core.Tracer here to identify jax arrays during jit tracing. From jax 0.8.2 on,
    # tracers are not a subclass of jax.Array anymore. Note that tracers can also represent
    # non-array values and a fully correct implementation would need to use isinstance checks. Since
    # we use hash-based caching with type names as keys, we cannot use instance checks without
    # losing performance here. For more information, see
    # https://github.com/data-apis/array-api-compat/pull/369 and the corresponding issue.
    return (
        _issubclass_fast(cls, "jax", "Array")
        or _issubclass_fast(cls, "jax.core", "Tracer")
        or _is_jax_zero_gradient_array(x)
    )

