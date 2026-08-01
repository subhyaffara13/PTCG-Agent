
def _set_to_cache(cache, key, graph, *, backend_name=None):
    """Set a backend graph to the cache, and remove unnecessary cached items.

    Parameters
    ----------
    cache : dict
        If ``backend_name`` is given, then this is treated as ``G.__networkx_cache__``,
        but if ``backend_name`` is None, then this is treated as the resolved inner
        cache such as ``G.__networkx_cache__["backends"][backend_name]``.
    key : tuple
        Cache key from ``_get_cache_key``.
    graph : graph or "FAILED_TO_CONVERT"
        Setting value to "FAILED_TO_CONVERT" prevents this conversion from being
        attempted in future calls.
    backend_name : str, optional
        Name of the backend to control how ``cache`` is interpreted.

    Returns
    -------
    dict
        The items that were removed from the cache.
    """
    if backend_name is not None:
        cache = cache.setdefault("backends", {}).setdefault(backend_name, {})
    # Remove old cached items that are no longer necessary since they
    # are dominated/subsumed/outdated by what was just calculated.
    # This uses the same logic as above, but with keys switched.
    # Also, don't update the cache here if the call will mutate an input.
    removed = {}
    edge_key, node_key = key
    cache[key] = graph  # Set at beginning to be thread-safe
    if graph == FAILED_TO_CONVERT:
        return removed
    for cur_key in list(cache):
        if cur_key == key:
            continue
        ekey, nkey = cur_key
        if ekey is False or edge_key is True:
            pass
        elif ekey is True or edge_key is False or not ekey.issubset(edge_key):
            continue
        if nkey is False or node_key is True:
            pass
        elif nkey is True or node_key is False or not nkey.issubset(node_key):
            continue
        # Use pop instead of del to try to be thread-safe
        if (graph := cache.pop(cur_key, None)) is not None:
            removed[cur_key] = graph
    return removed

