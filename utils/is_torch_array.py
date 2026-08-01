
def is_torch_array(x: object) -> TypeIs[torch.Tensor]:
    """
    Return True if `x` is a PyTorch tensor.

    This function does not import PyTorch if it has not already been imported
    and is therefore cheap to use.

    See Also
    --------

    array_namespace
    is_array_api_obj
    is_numpy_array
    is_cupy_array
    is_dask_array
    is_jax_array
    is_pydata_sparse_array
    """
    cls = cast(Hashable, type(x))
    return _issubclass_fast(cls, "torch", "Tensor")

