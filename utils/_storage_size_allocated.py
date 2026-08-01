
def _storage_size_allocated(tensor: Tensor):
    storage_size: int = tensor.untyped_storage().size()
    return storage_size > 0

