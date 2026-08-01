
def single_target_shortest_path_length(G, target, cutoff=None):
    """Compute the shortest path lengths to target from all reachable nodes.

    Parameters
    ----------
    G : NetworkX graph

    target : node
       Target node for path

    cutoff : integer, optional
        Depth to stop the search. Only source nodes where the shortest path
        from this node to the target node contains <= ``cutoff + 1`` nodes will
        be included in the returned results.

    Returns
    -------
    lengths : dictionary
        Dictionary, keyed by source, of shortest path lengths.

    Examples
    --------
    >>> G = nx.path_graph(5, create_using=nx.DiGraph())
    >>> length = nx.single_target_shortest_path_length(G, 4)
    >>> length[0]
    4
    >>> for node in sorted(length):
    ...     print(f"{node}: {length[node]}")
    0: 4
    1: 3
    2: 2
    3: 1
    4: 0

    Only include paths with length less than or equal to the `cutoff` keyword
    argument:

    >>> length = nx.single_target_shortest_path_length(G, 4, cutoff=2)
    >>> for node in sorted(length):
    ...     print(f"{node}: {length[node]}")
    2: 2
    3: 1
    4: 0

    See Also
    --------
    single_source_shortest_path_length, shortest_path_length
    """
    if target not in G:
        raise nx.NodeNotFound(f"Target {target} is not in G")
    if cutoff is None:
        cutoff = float("inf")
    # handle either directed or undirected
    adj = G._pred if G.is_directed() else G._adj
    nextlevel = [target]
    return dict(_single_shortest_path_length(adj, nextlevel, cutoff))

