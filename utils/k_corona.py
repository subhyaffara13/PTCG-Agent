
def k_corona(G, k, core_number=None):
    """Returns the k-corona of G.

    The k-corona is the subgraph of nodes in the k-core which have
    exactly k neighbors in the k-core.

    Parameters
    ----------
    G : NetworkX graph
       A graph or directed graph
    k : int
       The order of the corona.
    core_number : dictionary, optional
       Precomputed core numbers for the graph G.

    Returns
    -------
    G : NetworkX graph
       The k-corona subgraph

    Raises
    ------
    NetworkXNotImplemented
        The k-corona is not defined for multigraphs or graphs with self loops.

    Notes
    -----
    For directed graphs the node degree is defined to be the
    in-degree + out-degree.

    Graph, node, and edge attributes are copied to the subgraph.

    Examples
    --------
    >>> degrees = [0, 1, 2, 2, 2, 2, 3]
    >>> H = nx.havel_hakimi_graph(degrees)
    >>> H.degree
    DegreeView({0: 1, 1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 0})
    >>> nx.k_corona(H, k=2).nodes
    NodeView((1, 2, 3, 5))

    See Also
    --------
    core_number

    References
    ----------
    .. [1]  k -core (bootstrap) percolation on complex networks:
       Critical phenomena and nonlocal effects,
       A. V. Goltsev, S. N. Dorogovtsev, and J. F. F. Mendes,
       Phys. Rev. E 73, 056101 (2006)
       http://link.aps.org/doi/10.1103/PhysRevE.73.056101
    """

    def func(v, k, c):
        return c[v] == k and k == sum(1 for w in G[v] if c[w] >= k)

    return _core_subgraph(G, func, k, core_number)

