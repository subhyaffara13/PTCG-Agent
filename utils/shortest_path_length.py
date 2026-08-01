
def shortest_path_length(creation_sequence, i):
    """
    Return the shortest path length from indicated node to
    every other node for the threshold graph with the given
    creation sequence.
    Node is indicated by index i in creation_sequence unless
    creation_sequence is labeled in which case, i is taken to
    be the label of the node.

    Paths lengths in threshold graphs are at most 2.
    Length to unreachable nodes is set to -1.
    """
    # Turn input sequence into a labeled creation sequence
    first = creation_sequence[0]
    if isinstance(first, str):  # creation sequence
        if isinstance(creation_sequence, list):
            cs = creation_sequence[:]
        else:
            cs = list(creation_sequence)
    elif isinstance(first, tuple):  # labeled creation sequence
        cs = [v[1] for v in creation_sequence]
        i = [v[0] for v in creation_sequence].index(i)
    elif isinstance(first, int):  # compact creation sequence
        cs = uncompact(creation_sequence)
    else:
        raise TypeError("Not a valid creation sequence type")

    # Compute
    N = len(cs)
    spl = [2] * N  # length 2 to every node
    spl[i] = 0  # except self which is 0
    # 1 for all d's to the right
    for j in range(i + 1, N):
        if cs[j] == "d":
            spl[j] = 1
    if cs[i] == "d":  # 1 for all nodes to the left
        for j in range(i):
            spl[j] = 1
    # and -1 for any trailing i to indicate unreachable
    for j in range(N - 1, 0, -1):
        if cs[j] == "d":
            break
        spl[j] = -1
    return spl


def shortest_path_length(G, source=None, target=None, weight=None, method="dijkstra"):
    """Compute shortest path lengths in the graph.

    Parameters
    ----------
    G : NetworkX graph

    source : node, optional
        Starting node for path.
        If not specified, compute shortest path lengths using all nodes as
        source nodes.

    target : node, optional
        Ending node for path.
        If not specified, compute shortest path lengths using all nodes as
        target nodes.

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
        The algorithm to use to compute the path length.
        Supported options: 'dijkstra', 'bellman-ford'.
        Other inputs produce a ValueError.
        If `weight` is None, unweighted graph methods are used, and this
        suggestion is ignored.

    Returns
    -------
    length: number or iterator
        If the source and target are both specified, return the length of
        the shortest path from the source to the target.

        If only the source is specified, return a dict keyed by target
        to the shortest path length from the source to that target.

        If only the target is specified, return a dict keyed by source
        to the shortest path length from that source to the target.

        If neither the source nor target are specified, return an iterator
        over (source, dictionary) where dictionary is keyed by target to
        shortest path length from source to that target.

    Raises
    ------
    NodeNotFound
        If `source` is not in `G`.

    NetworkXNoPath
        If no path exists between source and target.

    ValueError
        If `method` is not among the supported options.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> nx.shortest_path_length(G, source=0, target=4)
    4
    >>> p = nx.shortest_path_length(G, source=0)  # target not specified
    >>> p[4]
    4
    >>> p = nx.shortest_path_length(G, target=4)  # source not specified
    >>> p[0]
    4
    >>> p = dict(nx.shortest_path_length(G))  # source,target not specified
    >>> p[0][4]
    4

    Notes
    -----
    The length of the path is always 1 less than the number of nodes involved
    in the path since the length measures the number of edges followed.

    For digraphs this returns the shortest directed path length. To find path
    lengths in the reverse direction use G.reverse(copy=False) first to flip
    the edge orientation.

    See Also
    --------
    all_pairs_shortest_path_length
    all_pairs_dijkstra_path_length
    all_pairs_bellman_ford_path_length
    single_source_shortest_path_length
    single_source_dijkstra_path_length
    single_source_bellman_ford_path_length
    """
    if method not in ("dijkstra", "bellman-ford"):
        # so we don't need to check in each branch later
        raise ValueError(f"method not supported: {method}")
    method = "unweighted" if weight is None else method
    if source is None:
        if target is None:
            # Find paths between all pairs.
            if method == "unweighted":
                paths = nx.all_pairs_shortest_path_length(G)
            elif method == "dijkstra":
                paths = nx.all_pairs_dijkstra_path_length(G, weight=weight)
            else:  # method == 'bellman-ford':
                paths = nx.all_pairs_bellman_ford_path_length(G, weight=weight)
        else:
            # Find paths from all nodes co-accessible to the target.
            if G.is_directed():
                G = G.reverse(copy=False)
            if method == "unweighted":
                path_length = nx.single_source_shortest_path_length
                paths = path_length(G, target)
            elif method == "dijkstra":
                path_length = nx.single_source_dijkstra_path_length
                paths = path_length(G, target, weight=weight)
            else:  # method == 'bellman-ford':
                path_length = nx.single_source_bellman_ford_path_length
                paths = path_length(G, target, weight=weight)
    else:
        if target is None:
            # Find paths to all nodes accessible from the source.
            if method == "unweighted":
                paths = nx.single_source_shortest_path_length(G, source)
            elif method == "dijkstra":
                path_length = nx.single_source_dijkstra_path_length
                paths = path_length(G, source, weight=weight)
            else:  # method == 'bellman-ford':
                path_length = nx.single_source_bellman_ford_path_length
                paths = path_length(G, source, weight=weight)
        else:
            # Find shortest source-target path.
            if method == "unweighted":
                p = nx.bidirectional_shortest_path(G, source, target)
                paths = len(p) - 1
            elif method == "dijkstra":
                paths = nx.dijkstra_path_length(G, source, target, weight)
            else:  # method == 'bellman-ford':
                paths = nx.bellman_ford_path_length(G, source, target, weight)
    return paths

