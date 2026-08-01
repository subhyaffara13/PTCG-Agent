
def get_cached_runtime(key: str) -> float | None:
    """Get cached runtime from process-local cache."""
    return _get_collective_cache().get(key)

