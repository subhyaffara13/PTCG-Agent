
def global_reaching_centrality(G, weight=None, normalized=True):
    """Returns the global reaching centrality of a directed graph.

    The *global reaching centrality* of a weighted directed graph is the
    average over all nodes of the difference between the local reaching
    centrality of the node and the greatest local reaching centrality of
    any node in the graph [1]_. For more information on the local
    reaching centrality, see :func:`local_reaching_centrality`.
    Informally, the local reaching centrality is the proportion of the
    graph that is reachable from the neighbors of the node.

    Parameters
    ----------
    G : DiGraph
        A networkx DiGraph.

    weight : None or string, optional (default=None)
        Attribute to use for edge weights. If ``None``, each edge weight
        is assumed to be one. A higher weight implies a stronger
        connection between nodes and a *shorter* path length.

    normalized : bool, optional (default=True)
        Whether to normalize the edge weights by the total sum of edge
        weights.

    Returns
    -------
    h : float
        The global reaching centrality of the graph.

    Examples
    --------
    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 2)
    >>> G.add_edge(1, 3)
    >>> nx.global_reaching_centrality(G)
    1.0
    >>> G.add_edge(3, 2)
    >>> nx.global_reaching_centrality(G)
    0.75

    See also
    --------
    local_reaching_centrality

    References
    ----------
    .. [1] Mones, Enys, Lilla Vicsek, and Tamás Vicsek.
           "Hierarchy Measure for Complex Networks."
           *PLoS ONE* 7.3 (2012): e33799.
           https://doi.org/10.1371/journal.pone.0033799
    """
    if nx.is_negatively_weighted(G, weight=weight):
        raise nx.NetworkXError("edge weights must be positive")
    total_weight = G.size(weight=weight)
    if total_weight <= 0:
        raise nx.NetworkXError("Size of G must be positive")
    # If provided, weights must be interpreted as connection strength
    # (so higher weights are more likely to be chosen). However, the
    # shortest path algorithms in NetworkX assume the provided "weight"
    # is actually a distance (so edges with higher weight are less
    # likely to be chosen). Therefore we need to invert the weights when
    # computing shortest paths.
    #
    # If weight is None, we leave it as-is so that the shortest path
    # algorithm can use a faster, unweighted algorithm.
    if weight is not None:

        def as_distance(u, v, d):
            return total_weight / d.get(weight, 1)

        shortest_paths = dict(nx.shortest_path(G, weight=as_distance))
    else:
        shortest_paths = dict(nx.shortest_path(G))

    centrality = local_reaching_centrality
    # TODO This can be trivially parallelized.
    lrc = [
        centrality(G, node, paths=paths, weight=weight, normalized=normalized)
        for node, paths in shortest_paths.items()
    ]

    max_lrc = max(lrc)
    return sum(max_lrc - c for c in lrc) / (len(G) - 1)

