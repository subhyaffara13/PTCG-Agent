
def single_source_shortest_path(G, source, cutoff=None):
    """Compute shortest path between source
    and all other nodes reachable from source.

    Parameters
    ----------
    G : NetworkX graph

    source : node label
       Starting node for path

    cutoff : integer, optional
        Depth to stop the search. Only target nodes where the shortest path to
        this node from the source node contains <= ``cutoff + 1`` nodes will be
        included in the returned results.

    Returns
    -------
    paths : dictionary
        Dictionary, keyed by target, of shortest paths.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> nx.single_source_shortest_path(G, 0)
    {0: [0], 1: [0, 1], 2: [0, 1, 2], 3: [0, 1, 2, 3], 4: [0, 1, 2, 3, 4]}

    Only include paths with length less than or equal to the `cutoff` keyword
    argument:

    >>> nx.single_source_shortest_path(G, 0, cutoff=2)
    {0: [0], 1: [0, 1], 2: [0, 1, 2]}

    Notes
    -----
    The shortest path is not necessarily unique. So there can be multiple
    paths between the source and each target node, all of which have the
    same 'shortest' length. For each target node, this function returns
    only one of those paths.

    See Also
    --------
    shortest_path
    """
    if source not in G:
        raise nx.NodeNotFound(f"Source {source} not in G")
    if cutoff is None:
        cutoff = float("inf")
    nextlevel = [source]  # list of nodes to check at next level
    paths = {source: [source]}  # paths dictionary  (paths to key from source)
    return dict(_single_shortest_path(G._adj, nextlevel, paths, cutoff, operator.add))

