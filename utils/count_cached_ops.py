
def count_cached_ops(cache: CacheType) -> CounterType[str]:
    """Returns a counter of the types of each op in the cache.
    This is useful for profiling to increase sharing.
    """
    return Counter(key[0] for key in cache.keys())

