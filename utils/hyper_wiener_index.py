
def hyper_wiener_index(G, weight=None):
    r"""Returns the Hyper-Wiener index of the graph `G`.

    The Hyper-Wiener index of a connected graph `G` is defined as

    .. math::
        WW(G) = \frac{1}{2} \sum_{u,v \in V(G)} (d(u,v) + d(u,v)^2)

    where ``d(u, v)`` is the shortest-path distance between nodes ``u`` and ``v``.

    Parameters
    ----------
    G : NetworkX graph
        An undirected, connected graph.

    weight : string or None, optional (default: None)
        The edge attribute to use for calculating shortest-path distances.
        If None, all edges are considered to have a weight of 1.

    Returns
    -------
    float
        The Hyper-Wiener index of the graph G.
        Returns float("inf") if the graph is not connected.

    References
    ----------
    .. [1] M. Randić, "Novel molecular descriptor for structure-property studies,"
           Chemical Physics Letters, vol. 211, pp. 478-483, 1993.
    .. [2] `Wikipedia: Hyper-Wiener Index <https://en.wikipedia.org/wiki/Hyper-Wiener_index>`_

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.hyper_wiener_index(G)
    30.0

    >>> G = nx.cycle_graph(4)
    >>> nx.hyper_wiener_index(G)
    20.0
    """
    if not nx.is_connected(G):
        return float("inf")

    spl = nx.shortest_path_length(G, weight=weight)
    total = sum(dist + dist**2 for _, lengths in spl for dist in lengths.values())
    return total / 2

