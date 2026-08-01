
def colliders(G):
    """Yields 3-node tuples that represent the colliders in `G`.

    In a Directed Acyclic Graph (DAG), if you have three nodes A, B, and C, and
    there are edges from A to C and from B to C, then C is a collider [1]_ . In
    a causal graph setting, this means that both events A and B are "causing" C,
    and conditioning on C provide an association between A and B even if
    no direct causal relationship exists between A and B.

    Parameters
    ----------
    G : graph
        A networkx `~networkx.DiGraph`.

    Yields
    ------
    A 3-tuple representation of a collider
        Each collider is a 3-tuple with the parent, collider, and other parent.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is an undirected graph.

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (0, 4), (3, 1), (2, 4), (0, 5), (4, 5), (1, 5)])
    >>> nx.is_directed_acyclic_graph(G)
    True
    >>> list(nx.dag.colliders(G))
    [(0, 4, 2), (0, 5, 4), (0, 5, 1), (4, 5, 1)]

    See Also
    --------
    v_structures

    Notes
    -----
    This function was written to be used on DAGs, however it works on cyclic graphs
    too. Since colliders are referred to in the cyclic causal graph literature
    [2]_ we allow cyclic graphs in this function. It is suggested that you test if
    your input graph is acyclic as in the example if you want that property.

    References
    ----------
    .. [1] `Wikipedia: Collider in causal graphs <https://en.wikipedia.org/wiki/Collider_(statistics)>`_
    .. [2] A Hyttinen, P.O. Hoyer, F. Eberhardt, M J ̈arvisalo, (2013)
           "Discovering cyclic causal models with latent variables:
           a general SAT-based procedure", UAI'13: Proceedings of the Twenty-Ninth
           Conference on Uncertainty in Artificial Intelligence, pg 301–310,
           `doi:10.5555/3023638.3023669 <https://dl.acm.org/doi/10.5555/3023638.3023669>`_
    """
    for node in G.nodes:
        for p1, p2 in combinations(G.predecessors(node), 2):
            yield (p1, node, p2)

