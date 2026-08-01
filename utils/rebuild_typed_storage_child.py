
def rebuild_typed_storage_child(storage, storage_type):
    return storage_type(wrap_storage=storage, _internal=True)

