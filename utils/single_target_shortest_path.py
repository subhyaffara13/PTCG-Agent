
def single_target_shortest_path(G, target, cutoff=None):
    """Compute shortest path to target from all nodes that reach target.

    Parameters
    ----------
    G : NetworkX graph

    target : node label
       Target node for path

    cutoff : integer, optional
        Depth to stop the search. Only source nodes where the shortest path
        from this node to the target node contains <= ``cutoff + 1`` nodes will
        be included in the returned results.

    Returns
    -------
    paths : dictionary
        Dictionary, keyed by source, of shortest paths.

    Examples
    --------
    >>> G = nx.path_graph(5, create_using=nx.DiGraph())
    >>> nx.single_target_shortest_path(G, 4)
    {4: [4], 3: [3, 4], 2: [2, 3, 4], 1: [1, 2, 3, 4], 0: [0, 1, 2, 3, 4]}

    Only include paths with length less than or equal to the `cutoff` keyword
    argument:

    >>> nx.single_target_shortest_path(G, 4, cutoff=2)
    {4: [4], 3: [3, 4], 2: [2, 3, 4]}

    Notes
    -----
    The shortest path is not necessarily unique. So there can be multiple
    paths between the source and each target node, all of which have the
    same 'shortest' length. For each target node, this function returns
    only one of those paths.

    See Also
    --------
    shortest_path, single_source_shortest_path
    """
    if target not in G:
        raise nx.NodeNotFound(f"Target {target} not in G")

    def join(p1, p2):
        return p2 + p1

    # handle undirected graphs
    adj = G._pred if G.is_directed() else G._adj
    if cutoff is None:
        cutoff = float("inf")
    nextlevel = [target]  # list of nodes to check at next level
    paths = {target: [target]}  # paths dictionary  (paths to key from source)
    return dict(_single_shortest_path(adj, nextlevel, paths, cutoff, join))

