
def v_structures(G):
    """Yields 3-node tuples that represent the v-structures in `G`.

    Colliders are triples in the directed acyclic graph (DAG) where two parent nodes
    point to the same child node. V-structures are colliders where the two parent
    nodes are not adjacent. In a causal graph setting, the parents do not directly
    depend on each other, but conditioning on the child node provides an association.

    Parameters
    ----------
    G : graph
        A networkx `~networkx.DiGraph`.

    Yields
    ------
    A 3-tuple representation of a v-structure
        Each v-structure is a 3-tuple with the parent, collider, and other parent.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is an undirected graph.

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (0, 4), (3, 1), (2, 4), (0, 5), (4, 5), (1, 5)])
    >>> nx.is_directed_acyclic_graph(G)
    True
    >>> list(nx.dag.v_structures(G))
    [(0, 4, 2), (0, 5, 1), (4, 5, 1)]

    See Also
    --------
    colliders

    Notes
    -----
    This function was written to be used on DAGs, however it works on cyclic graphs
    too. Since colliders are referred to in the cyclic causal graph literature
    [2]_ we allow cyclic graphs in this function. It is suggested that you test if
    your input graph is acyclic as in the example if you want that property.

    References
    ----------
    .. [1]  `Pearl's PRIMER <https://bayes.cs.ucla.edu/PRIMER/primer-ch2.pdf>`_
            Ch-2 page 50: v-structures def.
    .. [2] A Hyttinen, P.O. Hoyer, F. Eberhardt, M J ̈arvisalo, (2013)
           "Discovering cyclic causal models with latent variables:
           a general SAT-based procedure", UAI'13: Proceedings of the Twenty-Ninth
           Conference on Uncertainty in Artificial Intelligence, pg 301–310,
           `doi:10.5555/3023638.3023669 <https://dl.acm.org/doi/10.5555/3023638.3023669>`_
    """
    for p1, c, p2 in colliders(G):
        if not (G.has_edge(p1, p2) or G.has_edge(p2, p1)):
            yield (p1, c, p2)

