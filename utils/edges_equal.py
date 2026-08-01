
def edges_equal(edges1, edges2, *, directed=False):
    """Return whether edgelists are equal.

    Equality here means equal as Python objects. Edge data must match
    if included. Ordering of edges in an edgelist is not relevant;
    ordering of nodes in an edge is only relevant if ``directed == True``.

    Parameters
    ----------
    edges1, edges2 : iterables of tuples
        Each tuple can be
        an edge tuple ``(u, v)``, or
        an edge tuple with data `dict` s ``(u, v, d)``, or
        an edge tuple with keys and data `dict` s ``(u, v, k, d)``.

    directed : bool, optional (default=False)
        If `True`, edgelists are treated as coming from directed
        graphs.

    Returns
    -------
    bool
        `True` if edgelists are equal, `False` otherwise.

    Examples
    --------
    >>> G1 = nx.complete_graph(3)
    >>> G2 = nx.cycle_graph(3)
    >>> edges_equal(G1.edges, G2.edges)
    True

    Edge order is not taken into account:

    >>> G1 = nx.Graph([(0, 1), (1, 2)])
    >>> G2 = nx.Graph([(1, 2), (0, 1)])
    >>> edges_equal(G1.edges, G2.edges)
    True

    The `directed` parameter controls whether edges are treated as
    coming from directed graphs.

    >>> DG1 = nx.DiGraph([(0, 1)])
    >>> DG2 = nx.DiGraph([(1, 0)])
    >>> edges_equal(DG1.edges, DG2.edges, directed=False)  # Not recommended.
    True
    >>> edges_equal(DG1.edges, DG2.edges, directed=True)
    False

    This function is meant to be used on edgelists (i.e. the output of a
    ``G.edges()`` call), and can give unexpected results on unprocessed
    lists of edges:

    >>> l1 = [(0, 1)]
    >>> l2 = [(0, 1), (1, 0)]
    >>> edges_equal(l1, l2)  # Not recommended.
    False
    >>> G1 = nx.Graph(l1)
    >>> G2 = nx.Graph(l2)
    >>> edges_equal(G1.edges, G2.edges)
    True
    >>> DG1 = nx.DiGraph(l1)
    >>> DG2 = nx.DiGraph(l2)
    >>> edges_equal(DG1.edges, DG2.edges, directed=True)
    False
    """
    d1 = defaultdict(list)
    d2 = defaultdict(list)

    for e1, e2 in zip_longest(edges1, edges2, fillvalue=None):
        if e1 is None or e2 is None:
            return False  # One is longer.
        for e, d in [(e1, d1), (e2, d2)]:
            u, v, *data = e
            d[u, v].append(data)
            if not directed:
                d[v, u].append(data)

    # Can check one direction because lengths are the same.
    return all(d1[e].count(data) == d2[e].count(data) for e in d1 for data in d1[e])

