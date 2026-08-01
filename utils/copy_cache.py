
def copy_cache(
    cache: t.Optional[t.MutableMapping[t.Any, t.Any]],
) -> t.Optional[t.MutableMapping[t.Tuple["weakref.ref[t.Any]", str], "Template"]]:
    """Create an empty copy of the given cache."""
    if cache is None:
        return None

    if type(cache) is dict:  # noqa E721
        return {}

    return LRUCache(cache.capacity)  # type: ignore

