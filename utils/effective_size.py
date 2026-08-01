
def effective_size(G, nodes=None, weight=None):
    r"""Returns the effective size of all nodes in the graph ``G``.

    The *effective size* of a node's ego network is based on the concept
    of redundancy. A person's ego network has redundancy to the extent
    that her contacts are connected to each other as well. The
    nonredundant part of a person's relationships is the effective
    size of her ego network [1]_.  Formally, the effective size of a
    node $u$, denoted $e(u)$, is defined by

    .. math::

       e(u) = \sum_{v \in N(u) \setminus \{u\}}
       \left(1 - \sum_{w \in N(v)} p_{uw} m_{vw}\right)

    where $N(u)$ is the set of neighbors of $u$ and $p_{uw}$ is the
    normalized mutual weight of the (directed or undirected) edges
    joining $u$ and $v$, for each vertex $u$ and $v$ [1]_. And $m_{vw}$
    is the mutual weight of $v$ and $w$ divided by $v$ highest mutual
    weight with any of its neighbors. The *mutual weight* of $u$ and $v$
    is the sum of the weights of edges joining them (edge weights are
    assumed to be one if the graph is unweighted).

    For the case of unweighted and undirected graphs, Borgatti proposed
    a simplified formula to compute effective size [2]_

    .. math::

       e(u) = n - \frac{2t}{n}

    where `t` is the number of ties in the ego network (not including
    ties to ego) and `n` is the number of nodes (excluding ego).

    Parameters
    ----------
    G : NetworkX graph
        The graph containing ``v``. Directed graphs are treated like
        undirected graphs when computing neighbors of ``v``.

    nodes : container, optional
        Container of nodes in the graph ``G`` to compute the effective size.
        If None, the effective size of every node is computed.

    weight : None or string, optional
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.

    Returns
    -------
    dict
        Dictionary with nodes as keys and the effective size of the node as values.

    Notes
    -----
    Isolated nodes, including nodes which only have self-loop edges, do not
    have a well-defined effective size::

        >>> G = nx.path_graph(3)
        >>> G.add_edge(4, 4)
        >>> nx.effective_size(G)
        {0: 1.0, 1: 2.0, 2: 1.0, 4: nan}

    Burt also defined the related concept of *efficiency* of a node's ego
    network, which is its effective size divided by the degree of that
    node [1]_. So you can easily compute efficiency:

    >>> G = nx.DiGraph()
    >>> G.add_edges_from([(0, 1), (0, 2), (1, 0), (2, 1)])
    >>> esize = nx.effective_size(G)
    >>> efficiency = {n: v / G.degree(n) for n, v in esize.items()}

    See also
    --------
    constraint

    References
    ----------
    .. [1] Burt, Ronald S.
           *Structural Holes: The Social Structure of Competition.*
           Cambridge: Harvard University Press, 1995.

    .. [2] Borgatti, S.
           "Structural Holes: Unpacking Burt's Redundancy Measures"
           CONNECTIONS 20(1):35-38.
           http://www.analytictech.com/connections/v20(1)/holes.htm

    """

    def redundancy(G, u, v, weight=None):
        nmw = normalized_mutual_weight
        r = sum(
            nmw(G, u, w, weight=weight) * nmw(G, v, w, norm=max, weight=weight)
            for w in set(nx.all_neighbors(G, u))
        )
        return 1 - r

    # Check if scipy is available
    try:
        # Needed for errstate
        import numpy as np

        # make sure nx.adjacency_matrix will not raise
        import scipy as sp

        has_scipy = True
    except:
        has_scipy = False

    if nodes is None and has_scipy:
        # In order to compute constraint of all nodes,
        # algorithms based on sparse matrices can be much faster

        # Obtain the adjacency matrix
        P = nx.adjacency_matrix(G, weight=weight)

        # Calculate mutual weights
        mutual_weights1 = P + P.T
        mutual_weights2 = mutual_weights1.copy()

        with np.errstate(divide="ignore"):
            # Mutual_weights1 = Normalize mutual weights by row sums
            mutual_weights1 /= mutual_weights1.sum(axis=1)[:, np.newaxis]

            # Mutual_weights2 = Normalize mutual weights by row max
            mutual_weights2 /= mutual_weights2.max(axis=1).toarray()

        # Calculate effective sizes
        r = 1 - (mutual_weights1 @ mutual_weights2.T).toarray()
        effective_size = ((mutual_weights1 > 0) * r).sum(axis=1)

        # Special treatment: isolated nodes (ignoring selfloops) marked with "nan"
        sum_mutual_weights = mutual_weights1.sum(axis=1) - mutual_weights1.diagonal()
        isolated_nodes = sum_mutual_weights == 0
        effective_size[isolated_nodes] = float("nan")
        # Use tolist() to automatically convert numpy scalars -> Python scalars
        return dict(zip(G, effective_size.tolist()))

    # Results for only requested nodes
    effective_size = {}
    if nodes is None:
        nodes = G
    # Use Borgatti's simplified formula for unweighted and undirected graphs
    if not G.is_directed() and weight is None:
        for v in nodes:
            # Effective size is not defined for isolated nodes, including nodes
            # with only self-edges
            if all(u == v for u in G[v]):
                effective_size[v] = float("nan")
                continue
            E = nx.ego_graph(G, v, center=False, undirected=True)
            effective_size[v] = len(E) - (2 * E.size()) / len(E)
    else:
        for v in nodes:
            # Effective size is not defined for isolated nodes, including nodes
            # with only self-edges
            if all(u == v for u in G[v]):
                effective_size[v] = float("nan")
                continue
            effective_size[v] = sum(
                redundancy(G, v, u, weight) for u in set(nx.all_neighbors(G, v))
            )
    return effective_size

