
def generalized_petersen_graph(n, k, *, create_using=None):
    """
    Returns the Generalized Petersen Graph GP(n,k).

    The Generalized Peterson Graph consists of an outer cycle of n nodes
    connected to an inner circulant graph of n nodes, where nodes in the
    inner circulant are connected to their kth nearest neighbor [1]_ [2]_.
    A Generalized Petersen Graph is cubic with 2n nodes and 3n edges.

    Some well known graphs are examples of Generalized Petersen Graphs such
    as the Petersen Graph GP(5, 2), the Desargues graph GP(10, 3), the
    Moebius-Kantor graph GP(8, 3), and the dodecahedron graph GP(10, 2).

    Parameters
    ----------
    n : int
       Number of nodes in the outer cycle and inner circulant. ``n >= 3`` is required.

    k : int
       Neighbor to connect in the inner circulant. ``1 <= k <= n/2``.
       Note that some people require ``k < n/2`` but we and others allow equality.
       Also, ``k < n/2`` is equivalent to ``k <= floor((n-1)/2)``

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        Generalized Petersen Graph n k

    References
    ----------
    .. [1] https://mathworld.wolfram.com/GeneralizedPetersenGraph.html
    .. [2] https://en.wikipedia.org/wiki/Generalized_Petersen_graph
    """
    if n <= 2:
        raise NetworkXError(f"n >= 3 required. Got {n=}")
    if k < 1 or k > n / 2:
        raise NetworkXError(f" Got {n=} {k=}. Need 1 <= k <= n/2")

    G = nx.cycle_graph(range(n), create_using=create_using)  # u-nodes
    if G.is_directed():
        raise NetworkXError("Directed Graph not supported in create_using")
    for i in range(n):
        G.add_edge(i, n + i)  # add v-nodes and u to v edges
        G.add_edge(n + i, n + (i + k) % n)  # edge from v_i to v_(i+k)%n

    G.name = f"Generalized Petersen Graph GP({n}, {k})"
    return G

