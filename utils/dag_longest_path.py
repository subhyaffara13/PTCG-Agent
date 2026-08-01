
def dag_longest_path(G, weight="weight", default_weight=1, topo_order=None):
    """Returns the longest path in a directed acyclic graph (DAG).

    If `G` has edges with `weight` attribute the edge data are used as
    weight values.

    Parameters
    ----------
    G : NetworkX DiGraph
        A directed acyclic graph (DAG)

    weight : str, optional
        Edge data key to use for weight

    default_weight : int, optional
        The weight of edges that do not have a weight attribute

    topo_order: list or tuple, optional
        A topological order for `G` (if None, the function will compute one)

    Returns
    -------
    list
        Longest path

    Raises
    ------
    NetworkXNotImplemented
        If `G` is not directed

    Examples
    --------
    >>> DG = nx.DiGraph(
    ...     [(0, 1, {"cost": 1}), (1, 2, {"cost": 1}), (0, 2, {"cost": 42})]
    ... )
    >>> list(nx.all_simple_paths(DG, 0, 2))
    [[0, 1, 2], [0, 2]]
    >>> nx.dag_longest_path(DG)
    [0, 1, 2]
    >>> nx.dag_longest_path(DG, weight="cost")
    [0, 2]

    In the case where multiple valid topological orderings exist, `topo_order`
    can be used to specify a specific ordering:

    >>> DG = nx.DiGraph([(0, 1), (0, 2)])
    >>> sorted(nx.all_topological_sorts(DG))  # Valid topological orderings
    [[0, 1, 2], [0, 2, 1]]
    >>> nx.dag_longest_path(DG, topo_order=[0, 1, 2])
    [0, 1]
    >>> nx.dag_longest_path(DG, topo_order=[0, 2, 1])
    [0, 2]

    See also
    --------
    dag_longest_path_length

    """
    if not G:
        return []

    if topo_order is None:
        topo_order = nx.topological_sort(G)

    dist = {}  # stores {v : (length, u)}
    for v in topo_order:
        us = [
            (
                dist[u][0]
                + (
                    max(data.values(), key=lambda x: x.get(weight, default_weight))
                    if G.is_multigraph()
                    else data
                ).get(weight, default_weight),
                u,
            )
            for u, data in G.pred[v].items()
        ]

        # Use the best predecessor if there is one and its distance is
        # non-negative, otherwise terminate.
        maxu = max(us, key=lambda x: x[0]) if us else (0, v)
        dist[v] = maxu if maxu[0] >= 0 else (0, v)

    u = None
    v = max(dist, key=lambda x: dist[x][0])
    path = []
    while u != v:
        path.append(v)
        u = v
        v = dist[v][1]

    path.reverse()
    return path

