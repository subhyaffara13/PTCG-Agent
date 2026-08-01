
def shortest_path(creation_sequence, u, v):
    """
    Find the shortest path between u and v in a
    threshold graph G with the given creation_sequence.

    For an unlabeled creation_sequence, the vertices
    u and v must be integers in (0,len(sequence)) referring
    to the position of the desired vertices in the sequence.

    For a labeled creation_sequence, u and v are labels of vertices.

    Use cs=creation_sequence(degree_sequence,with_labels=True)
    to convert a degree sequence to a creation sequence.

    Returns a list of vertices from u to v.
    Example: if they are neighbors, it returns [u,v]
    """
    # Turn input sequence into a labeled creation sequence
    first = creation_sequence[0]
    if isinstance(first, str):  # creation sequence
        cs = [(i, creation_sequence[i]) for i in range(len(creation_sequence))]
    elif isinstance(first, tuple):  # labeled creation sequence
        cs = creation_sequence[:]
    elif isinstance(first, int):  # compact creation sequence
        ci = uncompact(creation_sequence)
        cs = [(i, ci[i]) for i in range(len(ci))]
    else:
        raise TypeError("Not a valid creation sequence type")

    verts = [s[0] for s in cs]
    if v not in verts:
        raise ValueError(f"Vertex {v} not in graph from creation_sequence")
    if u not in verts:
        raise ValueError(f"Vertex {u} not in graph from creation_sequence")
    # Done checking
    if u == v:
        return [u]

    uindex = verts.index(u)
    vindex = verts.index(v)
    bigind = max(uindex, vindex)
    if cs[bigind][1] == "d":
        return [u, v]
    # must be that cs[bigind][1]=='i'
    cs = cs[bigind:]
    while cs:
        vert = cs.pop()
        if vert[1] == "d":
            return [u, vert[0], v]
    # All after u are type 'i' so no connection
    return -1


def shortest_path(G, source=None, target=None, weight=None, method="dijkstra"):
    """Compute shortest paths in the graph.

    Parameters
    ----------
    G : NetworkX graph

    source : node, optional
        Starting node for path. If not specified, compute shortest
        paths for each possible starting node.

    target : node, optional
        Ending node for path. If not specified, compute shortest
        paths to all possible nodes.

    weight : None, string or function, optional (default = None)
        If None, every edge has weight/distance/cost 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.
        If this is a function, the weight of an edge is the value
        returned by the function. The function must accept exactly
        three positional arguments: the two endpoints of an edge and
        the dictionary of edge attributes for that edge.
        The function must return a number.

    method : string, optional (default = 'dijkstra')
        The algorithm to use to compute the path.
        Supported options: 'dijkstra', 'bellman-ford'.
        Other inputs produce a ValueError.
        If `weight` is None, unweighted graph methods are used, and this
        suggestion is ignored.

    Returns
    -------
    path: list or dictionary or iterator
        All returned paths include both the source and target in the path.

        If the source and target are both specified, return a single list
        of nodes in a shortest path from the source to the target.

        If only the source is specified, return a dictionary keyed by
        targets with a list of nodes in a shortest path from the source
        to one of the targets.

        If only the target is specified, return a dictionary keyed by
        sources with a list of nodes in a shortest path from one of the
        sources to the target.

        If neither the source nor target are specified, return an iterator
        over (source, dictionary) where dictionary is keyed by target to
        list of nodes in a shortest path from the source to the target.

    Raises
    ------
    NodeNotFound
        If `source` is not in `G`.

    ValueError
        If `method` is not among the supported options.

    NetworkXNoPath
       If `source` and `target` are specified but no path exists between them.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> print(nx.shortest_path(G, source=0, target=4))
    [0, 1, 2, 3, 4]
    >>> p = nx.shortest_path(G, source=0)  # target not specified
    >>> p[3]  # shortest path from source=0 to target=3
    [0, 1, 2, 3]
    >>> p = nx.shortest_path(G, target=4)  # source not specified
    >>> p[1]  # shortest path from source=1 to target=4
    [1, 2, 3, 4]
    >>> p = dict(nx.shortest_path(G))  # source, target not specified
    >>> p[2][4]  # shortest path from source=2 to target=4
    [2, 3, 4]

    Notes
    -----
    There may be more than one shortest path between a source and target.
    This returns only one of them.

    See Also
    --------
    all_pairs_shortest_path
    all_pairs_dijkstra_path
    all_pairs_bellman_ford_path
    single_source_shortest_path
    single_source_dijkstra_path
    single_source_bellman_ford_path
    """
    if method not in ("dijkstra", "bellman-ford"):
        # so we don't need to check in each branch later
        raise ValueError(f"method not supported: {method}")
    method = "unweighted" if weight is None else method
    if source is None:
        if target is None:
            # Find paths between all pairs. Iterator of dicts.
            if method == "unweighted":
                paths = nx.all_pairs_shortest_path(G)
            elif method == "dijkstra":
                paths = nx.all_pairs_dijkstra_path(G, weight=weight)
            else:  # method == 'bellman-ford':
                paths = nx.all_pairs_bellman_ford_path(G, weight=weight)
        else:
            # Find paths from all nodes co-accessible to the target.
            if G.is_directed():
                G = G.reverse(copy=False)
            if method == "unweighted":
                paths = nx.single_source_shortest_path(G, target)
            elif method == "dijkstra":
                paths = nx.single_source_dijkstra_path(G, target, weight=weight)
            else:  # method == 'bellman-ford':
                paths = nx.single_source_bellman_ford_path(G, target, weight=weight)
            # Now flip the paths so they go from a source to the target.
            for target in paths:
                paths[target] = list(reversed(paths[target]))
    else:
        if target is None:
            # Find paths to all nodes accessible from the source.
            if method == "unweighted":
                paths = nx.single_source_shortest_path(G, source)
            elif method == "dijkstra":
                paths = nx.single_source_dijkstra_path(G, source, weight=weight)
            else:  # method == 'bellman-ford':
                paths = nx.single_source_bellman_ford_path(G, source, weight=weight)
        else:
            # Find shortest source-target path.
            if method == "unweighted":
                paths = nx.bidirectional_shortest_path(G, source, target)
            elif method == "dijkstra":
                _, paths = nx.bidirectional_dijkstra(G, source, target, weight)
            else:  # method == 'bellman-ford':
                paths = nx.bellman_ford_path(G, source, target, weight)
    return paths

