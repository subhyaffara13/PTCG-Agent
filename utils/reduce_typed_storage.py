
def reduce_typed_storage(storage):
    return (rebuild_typed_storage, (storage._untyped_storage, storage.dtype))

