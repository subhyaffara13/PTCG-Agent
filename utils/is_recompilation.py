
def is_recompilation(cache_size: CacheSizeRelevantForFrame) -> bool:
    """
    If the frame (earlier parsed by compute_cache_size) has more than 1 cache
    entry with same ID_MATCH'd objects, then its a recompilation.
    """
    # Note that you can have multiple entries in the cache but still not a
    # recompile, e.g., you can have 64 nn module instances, each one having an
    # ID_MATCH guard, and each one having just 1 cache entry in the cache.  In
    # this case, we can have 64 entries in the cache, but no recompilation
    # because there is only one entry for each id_matched_obj.
    return cache_size.will_compilation_exceed(1)

