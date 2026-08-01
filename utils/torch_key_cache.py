
def torch_key_cache(func: Callable[[], bytes]) -> Callable[[], bytes]:
    """
    This function is a reimplementation of functools.lru_cache with a
    set function that allows prepopulating the cache.
    """
    # Use list for reference semantics
    _cache: list[bytes] = []

    def wrapper() -> bytes:
        if len(_cache) == 0:
            _cache.append(func())
        return _cache[0]

    def set_val(val: bytes) -> None:
        assert len(_cache) == 0
        _cache.append(val)

    def clear() -> None:
        _cache.clear()

    wrapper.set = set_val  # type: ignore[attr-defined]
    wrapper.clear = clear  # type: ignore[attr-defined]
    return wrapper

