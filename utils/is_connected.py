
def is_connected(G):
    """Returns True if the graph is connected, False otherwise.

    A graph is connected if, for every pair of distinct nodes, there is a
    path between them. If there is a pair of nodes for which such path does
    not exist, the graph is not connected (also referred to as "disconnected").

    A graph consisting of a single node and no edges is connected.
    Connectivity is undefined for the null graph (graph with no nodes).

    Parameters
    ----------
    G : NetworkX Graph
       An undirected graph.

    Returns
    -------
    connected : bool
      True if the graph is connected, False otherwise.

    Raises
    ------
    NetworkXNotImplemented
        If G is directed.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> print(nx.is_connected(G))
    True

    See Also
    --------
    is_strongly_connected
    is_weakly_connected
    is_semiconnected
    is_biconnected
    connected_components

    Notes
    -----
    This function is for undirected graphs only. For directed graphs, use
    :func:`is_strongly_connected` or :func:`is_weakly_connected`.

    The algorithm is based on a Breadth-First Search (BFS) traversal and its
    time complexity is $O(n + m)$, where $n$ is the number of nodes and $m$ the
    number of edges in the graph.

    """
    n = len(G)
    if n == 0:
        raise nx.NetworkXPointlessConcept(
            "Connectivity is undefined for the null graph."
        )
    return len(next(connected_components(G))) == n

