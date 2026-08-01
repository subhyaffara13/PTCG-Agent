
def minimal_branching(
    G, /, *, attr="weight", default=1, preserve_attrs=False, partition=None
):
    """
    Returns a minimal branching from `G`.

    A minimal branching is a branching similar to a minimal arborescence but
    without the requirement that the result is actually a spanning arborescence.
    This allows minimal branchinges to be computed over graphs which may not
    have arborescence (such as multiple components).

    Parameters
    ----------
    G : (multi)digraph-like
        The graph to be searched.
    attr : str
        The edge attribute used in determining optimality.
    default : float
        The value of the edge attribute used if an edge does not have
        the attribute `attr`.
    preserve_attrs : bool
        If True, preserve the other attributes of the original graph (that are not
        passed to `attr`)
    partition : str
        The key for the edge attribute containing the partition
        data on the graph. Edges can be included, excluded or open using the
        `EdgePartition` enum.

    Returns
    -------
    B : (multi)digraph-like
        A minimal branching.
    """
    max_weight = -INF
    min_weight = INF
    for _, _, w in G.edges(data=attr, default=default):
        if w > max_weight:
            max_weight = w
        if w < min_weight:
            min_weight = w

    for _, _, d in G.edges(data=True):
        # Transform the weights so that the minimum weight is larger than
        # the difference between the max and min weights. This is important
        # in order to prevent the edge weights from becoming negative during
        # computation
        d[attr] = max_weight + 1 + (max_weight - min_weight) - d.get(attr, default)
    nx._clear_cache(G)

    B = maximum_branching(G, attr, default, preserve_attrs, partition)

    # Reverse the weight transformations
    for _, _, d in G.edges(data=True):
        d[attr] = max_weight + 1 + (max_weight - min_weight) - d.get(attr, default)
    nx._clear_cache(G)

    for _, _, d in B.edges(data=True):
        d[attr] = max_weight + 1 + (max_weight - min_weight) - d.get(attr, default)
    nx._clear_cache(B)

    return B

