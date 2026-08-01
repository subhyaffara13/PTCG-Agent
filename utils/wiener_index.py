
def wiener_index(G, weight=None):
    """Returns the Wiener index of the given graph.

    The *Wiener index* of a graph is the sum of the shortest-path
    (weighted) distances between each pair of reachable nodes.
    For pairs of nodes in undirected graphs, only one orientation
    of the pair is counted.

    Parameters
    ----------
    G : NetworkX graph

    weight : string or None, optional (default: None)
        If None, every edge has weight 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.
        The edge weights are used to computing shortest-path distances.

    Returns
    -------
    number
        The Wiener index of the graph `G`.

    Raises
    ------
    NetworkXError
        If the graph `G` is not connected.

    Notes
    -----
    If a pair of nodes is not reachable, the distance is assumed to be
    infinity. This means that for graphs that are not
    strongly-connected, this function returns ``inf``.

    The Wiener index is not usually defined for directed graphs, however
    this function uses the natural generalization of the Wiener index to
    directed graphs.

    Examples
    --------
    The Wiener index of the (unweighted) complete graph on *n* nodes
    equals the number of pairs of the *n* nodes, since each pair of
    nodes is at distance one::

        >>> n = 10
        >>> G = nx.complete_graph(n)
        >>> nx.wiener_index(G) == n * (n - 1) / 2
        True

    Graphs that are not strongly-connected have infinite Wiener index::

        >>> G = nx.empty_graph(2)
        >>> nx.wiener_index(G)
        inf

    References
    ----------
    .. [1] `Wikipedia: Wiener Index <https://en.wikipedia.org/wiki/Wiener_index>`_
    """
    connected = nx.is_strongly_connected(G) if G.is_directed() else nx.is_connected(G)
    if not connected:
        return float("inf")

    spl = nx.shortest_path_length(G, weight=weight)
    total = sum(it.chain.from_iterable(nbrs.values() for node, nbrs in spl))
    # Need to account for double counting pairs of nodes in undirected graphs.
    return total if G.is_directed() else total / 2

