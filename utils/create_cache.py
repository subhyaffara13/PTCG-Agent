
def create_cache(
    size: int,
) -> t.Optional[t.MutableMapping[t.Tuple["weakref.ref[t.Any]", str], "Template"]]:
    """Return the cache class for the given size."""
    if size == 0:
        return None

    if size < 0:
        return {}

    return LRUCache(size)  # type: ignore


def create_cache(
    key: str,
    is_fbcode: bool,
    fb_cache_cls: str,
    oss_cache_cls: str,
) -> RemoteCache[JsonDataTy] | None:
    try:
        if is_fbcode:
            import torch._inductor.fb.remote_cache

            cache_cls = getattr(torch._inductor.fb.remote_cache, fb_cache_cls)
            return cache_cls(key)
        else:
            this_module = sys.modules[__name__]

            cache_cls = getattr(this_module, oss_cache_cls)
            return cache_cls(key)

    except Exception:
        log.warning("Unable to create a remote cache", exc_info=True)
        return None

