
def all_neighbors(graph, node):
    """Returns all of the neighbors of a node in the graph.

    If the graph is directed returns predecessors as well as successors.

    Parameters
    ----------
    graph : NetworkX graph
        Graph to find neighbors.
    node : node
        The node whose neighbors will be returned.

    Returns
    -------
    neighbors : iterator
        Iterator of neighbors

    Raises
    ------
    NetworkXError
        If `node` is not in the graph.

    Examples
    --------
    For undirected graphs, this function is equivalent to ``G.neighbors(node)``.

    >>> G = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
    >>> list(nx.all_neighbors(G, 1))
    [0, 2]

    For directed graphs, this function returns both predecessors and successors,
    which may include duplicates if a node is both a predecessor and successor
    (e.g., in bidirectional edges or self-loops).

    >>> DG = nx.DiGraph([(0, 1), (1, 2), (2, 1)])
    >>> list(nx.all_neighbors(DG, 1))
    [0, 2, 2]

    Notes
    -----
    This function iterates over all neighbors (both predecessors and successors).

    See Also
    --------
    Graph.neighbors : Returns successors for both Graph and DiGraph
    DiGraph.predecessors : Returns predecessors for directed graphs only
    DiGraph.successors : Returns successors for directed graphs only
    """
    if graph.is_directed():
        values = chain(graph.predecessors(node), graph.successors(node))
    else:
        values = graph.neighbors(node)
    return values

