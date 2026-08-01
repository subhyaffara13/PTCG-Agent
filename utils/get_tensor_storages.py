
def get_tensor_storages(tensor: torch.Tensor) -> set[StorageWeakRef]:
    """
    Get storage references from a tensor.

    Handles regular tensors. Raises NotImplementedError for sparse tensors
    and traceable wrapper subclasses.

    Args:
        tensor: The tensor to extract storages from

    Returns:
        Set of StorageWeakRef objects for the tensor's storage(s)
    """
    from torch.multiprocessing.reductions import StorageWeakRef
    from torch.utils._python_dispatch import is_traceable_wrapper_subclass

    storages: set[StorageWeakRef] = set()

    if not isinstance(tensor, torch.Tensor):
        return storages

    if tensor.is_sparse or tensor.is_sparse_csr:
        raise NotImplementedError("get_tensor_storages does not support sparse tensors")

    if is_traceable_wrapper_subclass(tensor):
        raise NotImplementedError(
            "get_tensor_storages does not support traceable wrapper subclasses"
        )
    else:
        storages.add(StorageWeakRef(tensor._typed_storage()))

    return storages

