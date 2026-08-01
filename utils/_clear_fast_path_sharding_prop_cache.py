
def _clear_fast_path_sharding_prop_cache():
    """
    Clears the cache for the fast path sharding propagation cache, used for debugging purpose only.
    """
    torch._C._clear_DTensor_sharding_propagator_cache()

