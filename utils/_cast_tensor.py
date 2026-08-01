
def _cast_tensor(tensor: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    """
    Casts the underlying storage to a tensor of the given dtype.

    The returned tensor will be of size ``storage.nbytes``.

    This works for all datatypes and supports strided/offset tensors with the
    caveat that the cast tensor may be larger than the original tensor due to
    the differences in striding.
    """
    if type(tensor) is not torch.Tensor:
        raise AssertionError(f"can only cast standard tensors not {type(tensor)}")
    storage = tensor.untyped_storage()
    ret = torch.tensor(storage, dtype=dtype, device=tensor.device)
    if ret.untyped_storage() is not storage:
        raise AssertionError("storage should be the same")
    return ret

