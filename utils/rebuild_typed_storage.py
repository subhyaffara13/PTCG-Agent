
def rebuild_typed_storage(storage, dtype):
    return torch.storage.TypedStorage(wrap_storage=storage, dtype=dtype, _internal=True)

