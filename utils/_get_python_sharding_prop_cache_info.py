
def _get_python_sharding_prop_cache_info():
    """
    Get the cache info for the Python sharding propagation cache, used for debugging purpose only.
    This would return a named tuple showing hits, misses, maxsize and cursize of the sharding
    propagator cache. Note that directly calling into the sharding propagator does not share cache
    state with the DTensor dispatch fast path!
    """
    from torch.distributed.tensor._api import DTensor

    return (
        DTensor._op_dispatcher.sharding_propagator.propagate_op_sharding.cache_info()  # type:ignore[attr-defined]
    )

