
def number_connected_components(G):
    """Returns the number of connected components.

    The connected components of an undirected graph partition the graph into
    disjoint sets of nodes. Each of these sets induces a subgraph of graph
    `G` that is connected and not part of any larger connected subgraph.

    A graph is connected (:func:`is_connected`) if, for every pair of distinct
    nodes, there is a path between them. If there is a pair of nodes for
    which such path does not exist, the graph is not connected (also referred
    to as "disconnected").

    A graph consisting of a single node and no edges is connected.
    Connectivity is undefined for the null graph (graph with no nodes).

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph.

    Returns
    -------
    n : integer
       Number of connected components

    Raises
    ------
    NetworkXNotImplemented
        If G is directed.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (1, 2), (5, 6), (3, 4)])
    >>> nx.number_connected_components(G)
    3

    See Also
    --------
    connected_components
    is_connected
    number_weakly_connected_components
    number_strongly_connected_components

    Notes
    -----
    This function is for undirected graphs only. For directed graphs, use
    :func:`number_strongly_connected_components` or
    :func:`number_weakly_connected_components`.

    The algorithm is based on a Breadth-First Search (BFS) traversal and its
    time complexity is $O(n + m)$, where $n$ is the number of nodes and $m$ the
    number of edges in the graph.

    """
    return sum(1 for _ in connected_components(G))

