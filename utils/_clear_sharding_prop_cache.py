
def _clear_sharding_prop_cache():
    """
    Clears both the Python and fast path sharding propagation caches, used for debugging purpose only.
    This is the recommended way to clear all sharding propagation caches.
    """
    _clear_python_sharding_prop_cache()
    _clear_fast_path_sharding_prop_cache()

