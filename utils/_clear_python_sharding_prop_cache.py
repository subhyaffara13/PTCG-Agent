
def _clear_python_sharding_prop_cache():
    """
    Clears the cache for the Python sharding propagation cache, used for debugging purpose only.
    """
    from torch.distributed.tensor._api import DTensor

    return (
        DTensor._op_dispatcher.sharding_propagator.propagate_op_sharding.cache_clear()  # type:ignore[attr-defined]
    )

