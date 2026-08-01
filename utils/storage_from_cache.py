
def storage_from_cache(cls, key):
    storage_ref = shared_cache.get(key)
    if storage_ref is None:
        return None
    return torch.UntypedStorage._new_with_weak_ptr(storage_ref.cdata)

