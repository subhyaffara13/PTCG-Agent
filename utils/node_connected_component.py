
def node_connected_component(G, n):
    """Returns the set of nodes in the component of graph containing node n.

    A connected component is a set of nodes that induces a subgraph of graph
    `G` that is connected and not part of any larger connected subgraph.

    A graph is connected (:func:`is_connected`) if, for every pair of distinct
    nodes, there is a path between them. If there is a pair of nodes for
    which such path does not exist, the graph is not connected (also referred
    to as "disconnected").

    A graph consisting of a single node and no edges is connected.
    Connectivity is undefined for the null graph (graph with no nodes).

    Parameters
    ----------
    G : NetworkX Graph
       An undirected graph.

    n : node label
       A node in G

    Returns
    -------
    comp : set
       A set of nodes in the component of G containing node n.

    Raises
    ------
    NetworkXNotImplemented
        If G is directed.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (1, 2), (5, 6), (3, 4)])
    >>> nx.node_connected_component(G, 0)  # nodes of component that contains node 0
    {0, 1, 2}

    See Also
    --------
    connected_components

    Notes
    -----
    This function is for undirected graphs only.

    The algorithm is based on a Breadth-First Search (BFS) traversal and its
    time complexity is $O(n + m)$, where $n$ is the number of nodes and $m$ the
    number of edges in the graph.

    """
    return _plain_bfs(G, len(G), n)

