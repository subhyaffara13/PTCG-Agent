
def rebuild_storage_filename(cls, manager, handle, size, dtype=None):
    storage: torch.TypedStorage | torch.UntypedStorage = storage_from_cache(cls, handle)
    if storage is not None:
        return storage._shared_decref()
    if dtype is None:
        storage = torch.UntypedStorage._new_shared_filename_cpu(manager, handle, size)
    else:
        byte_size = size * torch._utils._element_size(dtype)
        untyped_storage: torch.UntypedStorage = (
            torch.UntypedStorage._new_shared_filename_cpu(manager, handle, byte_size)
        )
        storage = torch.TypedStorage(
            wrap_storage=untyped_storage, dtype=dtype, _internal=True
        )
    shared_cache[handle] = StorageWeakRef(storage)
    return storage._shared_decref()

