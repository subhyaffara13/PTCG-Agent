
def single_source_shortest_path_length(G, source, cutoff=None):
    """Compute the shortest path lengths from `source` to all reachable nodes in `G`.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Starting node for path

    cutoff : integer, optional
        Depth to stop the search. Only target nodes where the shortest path to
        this node from the source node contains <= ``cutoff + 1`` nodes will be
        included in the returned results.

    Returns
    -------
    lengths : dict
        Dict keyed by node to shortest path length from source node.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> length = nx.single_source_shortest_path_length(G, 0)
    >>> length[4]
    4
    >>> for node in sorted(length):
    ...     print(f"{node}: {length[node]}")
    0: 0
    1: 1
    2: 2
    3: 3
    4: 4

    Only include paths with length less than or equal to the `cutoff` keyword
    argument:

    >>> length = nx.single_source_shortest_path_length(G, 0, cutoff=2)
    >>> for node in sorted(length):
    ...     print(f"{node}: {length[node]}")
    0: 0
    1: 1
    2: 2

    See Also
    --------
    :any:`shortest_path_length` :
       Shortest path length with specifiable source, target, and weight.
    :any:`single_source_dijkstra_path_length` :
       Shortest weighted path length from source with Dijkstra algorithm.
    :any:`single_source_bellman_ford_path_length` :
       Shortest weighted path length from source with Bellman-Ford algorithm.
    """
    if source not in G:
        raise nx.NodeNotFound(f"Source {source} is not in G")
    if cutoff is None:
        cutoff = float("inf")
    nextlevel = [source]
    return dict(_single_shortest_path_length(G._adj, nextlevel, cutoff))

