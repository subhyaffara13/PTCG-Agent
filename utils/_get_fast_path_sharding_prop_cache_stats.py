
def _get_fast_path_sharding_prop_cache_stats():
    """
    Get a tuple (hits, misses) for the fast path sharding propagation cache, used for debugging
    only.
    """
    return torch._C._get_DTensor_sharding_propagator_cache_stats()

