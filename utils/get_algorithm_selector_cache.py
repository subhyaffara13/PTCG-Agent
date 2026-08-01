
def get_algorithm_selector_cache() -> AlgorithmSelectorCache:
    """Get the global algorithm selector cache, creating it if it doesn't exist."""
    global _ALGORITHM_SELECTOR_CACHE
    if _ALGORITHM_SELECTOR_CACHE is None:
        _ALGORITHM_SELECTOR_CACHE = AlgorithmSelectorCache()
    return _ALGORITHM_SELECTOR_CACHE

