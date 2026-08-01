
def get_cached_should_pad(key: str) -> bool:
    return get_pad_cache().lookup(key)  # type: ignore[return-value]

