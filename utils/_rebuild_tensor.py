
def _rebuild_tensor(storage, storage_offset, size, stride):
    # first construct a tensor with the correct dtype/device
    t = torch.empty((0,), dtype=storage.dtype, device=storage._untyped_storage.device)
    return t.set_(storage._untyped_storage, storage_offset, size, stride)

