
def _save_tensors(*tensors: ArrayType) -> None:
    """Save tensors in the cache to prevent their ids from being recycled.
    This is needed to prevent false cache lookups.
    """
    cache = get_sharing_cache()
    for tensor in tensors:
        cache["tensor", id(tensor)] = tensor

