
def resistance_distance(G, nodeA=None, nodeB=None, weight=None, invert_weight=True):
    """Returns the resistance distance between pairs of nodes in graph G.

    The resistance distance between two nodes of a graph is akin to treating
    the graph as a grid of resistors with a resistance equal to the provided
    weight [1]_, [2]_.

    If weight is not provided, then a weight of 1 is used for all edges.

    If two nodes are the same, the resistance distance is zero.

    Parameters
    ----------
    G : NetworkX graph
       A graph

    nodeA : node or None, optional (default=None)
      A node within graph G.
      If None, compute resistance distance using all nodes as source nodes.

    nodeB : node or None, optional (default=None)
      A node within graph G.
      If None, compute resistance distance using all nodes as target nodes.

    weight : string or None, optional (default=None)
       The edge data key used to compute the resistance distance.
       If None, then each edge has weight 1.

    invert_weight : boolean (default=True)
        Proper calculation of resistance distance requires building the
        Laplacian matrix with the reciprocal of the weight. Not required
        if the weight is already inverted. Weight cannot be zero.

    Returns
    -------
    rd : dict or float
       If `nodeA` and `nodeB` are given, resistance distance between `nodeA`
       and `nodeB`. If `nodeA` or `nodeB` is unspecified (the default), a
       dictionary of nodes with resistance distances as the value.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is a directed graph.

    NetworkXError
        If `G` is not connected, or contains no nodes,
        or `nodeA` is not in `G` or `nodeB` is not in `G`.

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (4, 5)])
    >>> round(nx.resistance_distance(G, 1, 3), 10)
    0.625

    Notes
    -----
    The implementation is based on Theorem A in [2]_. Self-loops are ignored.
    Multi-edges are contracted in one edge with weight equal to the harmonic sum of the weights.

    References
    ----------
    .. [1] Wikipedia
       "Resistance distance."
       https://en.wikipedia.org/wiki/Resistance_distance
    .. [2] D. J. Klein and M. Randic.
        Resistance distance.
        J. of Math. Chem. 12:81-95, 1993.
    """
    import numpy as np

    if len(G) == 0:
        raise nx.NetworkXError("Graph G must contain at least one node.")
    if not nx.is_connected(G):
        raise nx.NetworkXError("Graph G must be strongly connected.")
    if nodeA is not None and nodeA not in G:
        raise nx.NetworkXError("Node A is not in graph G.")
    if nodeB is not None and nodeB not in G:
        raise nx.NetworkXError("Node B is not in graph G.")

    G = G.copy()
    node_list = list(G)

    # Invert weights
    if invert_weight and weight is not None:
        if G.is_multigraph():
            for u, v, k, d in G.edges(keys=True, data=True):
                d[weight] = 1 / d[weight]
        else:
            for u, v, d in G.edges(data=True):
                d[weight] = 1 / d[weight]

    # Compute resistance distance using the Pseudo-inverse of the Laplacian
    # Self-loops are ignored
    L = nx.laplacian_matrix(G, weight=weight).todense()
    Linv = np.linalg.pinv(L, hermitian=True)

    # Return relevant distances
    if nodeA is not None and nodeB is not None:
        i = node_list.index(nodeA)
        j = node_list.index(nodeB)
        return Linv.item(i, i) + Linv.item(j, j) - Linv.item(i, j) - Linv.item(j, i)

    elif nodeA is not None:
        i = node_list.index(nodeA)
        d = {}
        for n in G:
            j = node_list.index(n)
            d[n] = Linv.item(i, i) + Linv.item(j, j) - Linv.item(i, j) - Linv.item(j, i)
        return d

    elif nodeB is not None:
        j = node_list.index(nodeB)
        d = {}
        for n in G:
            i = node_list.index(n)
            d[n] = Linv.item(i, i) + Linv.item(j, j) - Linv.item(i, j) - Linv.item(j, i)
        return d

    else:
        d = {}
        for n in G:
            i = node_list.index(n)
            d[n] = {}
            for n2 in G:
                j = node_list.index(n2)
                d[n][n2] = (
                    Linv.item(i, i)
                    + Linv.item(j, j)
                    - Linv.item(i, j)
                    - Linv.item(j, i)
                )
        return d

