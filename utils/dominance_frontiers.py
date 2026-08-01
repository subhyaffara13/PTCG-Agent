
def dominance_frontiers(G, start):
    """Returns the dominance frontiers of all nodes of a directed graph.

    Parameters
    ----------
    G : a DiGraph or MultiDiGraph
        The graph where dominance is to be computed.

    start : node
        The start node of dominance computation.

    Returns
    -------
    df : dict keyed by nodes
        A dict containing the dominance frontiers of each node reachable from
        `start` as lists.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is undirected.

    NetworkXError
        If `start` is not in `G`.

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (1, 3), (2, 5), (3, 4), (4, 5)])
    >>> sorted((u, sorted(df)) for u, df in nx.dominance_frontiers(G, 1).items())
    [(1, []), (2, [5]), (3, [5]), (4, [5]), (5, [])]

    References
    ----------
    .. [1] Cooper, Keith D., Harvey, Timothy J. and Kennedy, Ken.
           "A simple, fast dominance algorithm." (2006).
           https://hdl.handle.net/1911/96345
    """
    idom = nx.immediate_dominators(G, start) | {start: None}

    df = {u: set() for u in idom}
    for u in idom:
        if u == start or len(G.pred[u]) >= 2:
            for v in G.pred[u]:
                if v in idom:
                    while v != idom[u]:
                        df[v].add(u)
                        v = idom[v]
    return df

