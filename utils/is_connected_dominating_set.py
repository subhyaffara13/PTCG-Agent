
def is_connected_dominating_set(G, nbunch):
    """Checks if `nbunch` is a connected dominating set for `G`.

    A *dominating set* for a graph *G* with node set *V* is a subset *D* of
    *V* such that every node not in *D* is adjacent to at least one
    member of *D* [1]_. A *connected dominating set* is a dominating
    set *C* that induces a connected subgraph of *G* [2]_.

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph.

    nbunch : iterable
        An iterable of nodes in the graph `G`.

    Returns
    -------
    connected_dominating : bool
        True if `nbunch` is connected dominating set of `G`, false otherwise.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Dominating_set
    .. [2] https://en.wikipedia.org/wiki/Connected_dominating_set

    """
    return nx.is_dominating_set(G, nbunch) and nx.is_connected(nx.subgraph(G, nbunch))

