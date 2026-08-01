
def _tensor_storage(t) -> StorageWeakRef:
    return StorageWeakRef(t._typed_storage())

