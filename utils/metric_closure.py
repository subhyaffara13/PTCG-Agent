
def metric_closure(G, weight="weight"):
    """Return the metric closure of a graph.

    The metric closure of a graph *G* is the complete graph in which each edge
    is weighted by the shortest path distance between the nodes in *G* .

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    NetworkX graph
        Metric closure of the graph `G`.

    Notes
    -----
    .. deprecated:: 3.6
       `metric_closure` is deprecated and will be removed in NetworkX 3.8.
       Use :func:`networkx.all_pairs_shortest_path_length` instead.

    """
    import warnings

    warnings.warn(
        "metric_closure is deprecated and will be removed in NetworkX 3.8.\n"
        "Use nx.all_pairs_shortest_path_length instead.",
        category=DeprecationWarning,
        stacklevel=5,
    )

    M = nx.Graph()

    Gnodes = set(G)

    # check for connected graph while processing first node
    all_paths_iter = nx.all_pairs_dijkstra(G, weight=weight)
    u, (distance, path) = next(all_paths_iter)
    if len(G) != len(distance):
        msg = "G is not a connected graph. metric_closure is not defined."
        raise nx.NetworkXError(msg)
    Gnodes.remove(u)
    for v in Gnodes:
        M.add_edge(u, v, distance=distance[v], path=path[v])

    # first node done -- now process the rest
    for u, (distance, path) in all_paths_iter:
        Gnodes.remove(u)
        for v in Gnodes:
            M.add_edge(u, v, distance=distance[v], path=path[v])

    return M

