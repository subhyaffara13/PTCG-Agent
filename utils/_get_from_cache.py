import itertools

def _get_from_cache(cache, key, *, backend_name=None, mutations=None):
    """Search the networkx cache for a graph that is compatible with ``key``.

    Parameters
    ----------
    cache : dict
        If ``backend_name`` is given, then this is treated as ``G.__networkx_cache__``,
        but if ``backend_name`` is None, then this is treated as the resolved inner
        cache such as ``G.__networkx_cache__["backends"][backend_name]``.
    key : tuple
        Cache key from ``_get_cache_key``.
    backend_name : str, optional
        Name of the backend to control how ``cache`` is interpreted.
    mutations : list, optional
        Used internally to clear objects gotten from cache if inputs will be mutated.

    Returns
    -------
    tuple or None
        The key of the compatible graph found in the cache.
    graph or "FAILED_TO_CONVERT" or None
        A compatible graph if possible. "FAILED_TO_CONVERT" indicates that a previous
        conversion attempt failed for this cache key.
    """
    if backend_name is not None:
        cache = cache.get("backends", {}).get(backend_name, {})
    if not cache:
        return None, None

    # Do a simple search for a cached graph with compatible data.
    # For example, if we need a single attribute, then it's okay
    # to use a cached graph that preserved all attributes.
    # This looks for an exact match first.
    edge_key, node_key = key
    for compat_key in itertools.product(
        (edge_key, True) if edge_key is not True else (True,),
        (node_key, True) if node_key is not True else (True,),
    ):
        if (rv := cache.get(compat_key)) is not None and (
            rv != FAILED_TO_CONVERT or key == compat_key
        ):
            if mutations is not None:
                # Remove this item from the cache (after all conversions) if
                # the call to this dispatchable function will mutate an input.
                mutations.append((cache, compat_key))
            return compat_key, rv

    # Iterate over the items in `cache` to see if any are compatible.
    # For example, if no edge attributes are needed, then a graph
    # with any edge attribute will suffice. We use the same logic
    # below (but switched) to clear unnecessary items from the cache.
    # Use `list(cache.items())` to be thread-safe.
    for (ekey, nkey), graph in list(cache.items()):
        if graph == FAILED_TO_CONVERT:
            # Return FAILED_TO_CONVERT if any cache key that requires a subset
            # of the edge/node attributes of the given cache key has previously
            # failed to convert. This logic is similar to `_set_to_cache`.
            if ekey is False or edge_key is True:
                pass
            elif ekey is True or edge_key is False or not ekey.issubset(edge_key):
                continue
            if nkey is False or node_key is True:  # or nkey == node_key:
                pass
            elif nkey is True or node_key is False or not nkey.issubset(node_key):
                continue
            # Save to cache for faster subsequent lookups
            cache[key] = FAILED_TO_CONVERT
        elif edge_key is False or ekey is True:
            pass  # Cache works for edge data!
        elif edge_key is True or ekey is False or not edge_key.issubset(ekey):
            continue  # Cache missing required edge data; does not work
        if node_key is False or nkey is True:
            pass  # Cache works for node data!
        elif node_key is True or nkey is False or not node_key.issubset(nkey):
            continue  # Cache missing required node data; does not work
        if mutations is not None:
            # Remove this item from the cache (after all conversions) if
            # the call to this dispatchable function will mutate an input.
            mutations.append((cache, (ekey, nkey)))
        return (ekey, nkey), graph

    return None, None

