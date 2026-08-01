
def get_exc_type(cls: Type[Exception]) -> str:
    # slightly more efficient than using lru_cache since we don't need to worry about the cache filling up
    try:
        return _EXC_TYPE_CACHE[cls]
    except KeyError:
        r = _get_exc_type(cls)
        _EXC_TYPE_CACHE[cls] = r
        return r

