
def disjoint_union_all(graphs):
    """Returns the disjoint union of all graphs.

    This operation forces distinct integer node labels starting with 0
    for the first graph in the list and numbering consecutively.

    Parameters
    ----------
    graphs : iterable
       Iterable of NetworkX graphs

    Returns
    -------
    U : A graph with the same type as the first graph in list

    Raises
    ------
    ValueError
       If `graphs` is an empty list.

    NetworkXError
        In case of mixed type graphs, like MultiGraph and Graph, or directed and undirected graphs.

    Examples
    --------
    >>> G1 = nx.Graph([(1, 2), (2, 3)])
    >>> G2 = nx.Graph([(4, 5), (5, 6)])
    >>> U = nx.disjoint_union_all([G1, G2])
    >>> list(U.nodes())
    [0, 1, 2, 3, 4, 5]
    >>> list(U.edges())
    [(0, 1), (1, 2), (3, 4), (4, 5)]

    Notes
    -----
    For operating on mixed type graphs, they should be converted to the same type.

    Graph, edge, and node attributes are propagated to the union graph.
    If a graph attribute is present in multiple graphs, then the value
    from the last graph in the list with that attribute is used.
    """

    def yield_relabeled(graphs):
        first_label = 0
        for G in graphs:
            yield nx.convert_node_labels_to_integers(G, first_label=first_label)
            first_label += len(G)

    R = union_all(yield_relabeled(graphs))

    return R

