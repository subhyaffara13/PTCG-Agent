
def id_tensor_storage(tensor: torch.Tensor) -> tuple[torch.device, int, int]:
    """
    Unique identifier to a tensor storage. Multiple different tensors can share the same underlying storage. For
    example, "meta" tensors all share the same storage, and thus their identifier will all be equal. This identifier is
    guaranteed to be unique and constant for this tensor's storage during its lifetime. Two tensor storages with
    non-overlapping lifetimes may have the same id.
    """
    if _torch_distributed_available and is_torch_greater_or_equal("2.5"):
        from torch.distributed.tensor import DTensor

        if isinstance(tensor, DTensor):
            local_tensor = tensor.to_local()
            return tensor.device, local_tensor.storage().data_ptr(), tensor.nbytes

    if tensor.device.type == "xla" and is_torch_xla_available():
        # NOTE: xla tensors dont have storage
        # use some other unique id to distinguish.
        # this is a XLA tensor, it must be created using torch_xla's
        # device. So the following import is safe:
        import torch_xla

        unique_id = torch_xla._XLAC._xla_get_tensor_id(tensor)
    else:
        unique_id = storage_ptr(tensor)

    return tensor.device, unique_id, storage_size(tensor)

