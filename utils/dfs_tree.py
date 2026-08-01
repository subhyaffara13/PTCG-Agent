
def dfs_tree(G, source=None, depth_limit=None, *, sort_neighbors=None):
    """Returns oriented tree constructed from a depth-first-search from source.

    Parameters
    ----------
    G : NetworkX graph

    source : node, optional
       Specify starting node for depth-first search.

    depth_limit : int, optional (default=len(G))
       Specify the maximum search depth.

    sort_neighbors : function (default=None)
        A function that takes an iterator over nodes as the input, and
        returns an iterable of the same nodes with a custom ordering.
        For example, `sorted` will sort the nodes in increasing order.

    Returns
    -------
    T : NetworkX DiGraph
       An oriented tree

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> T = nx.dfs_tree(G, source=0, depth_limit=2)
    >>> list(T.edges())
    [(0, 1), (1, 2)]
    >>> T = nx.dfs_tree(G, source=0)
    >>> list(T.edges())
    [(0, 1), (1, 2), (2, 3), (3, 4)]

    See Also
    --------
    dfs_preorder_nodes
    dfs_postorder_nodes
    dfs_labeled_edges
    :func:`~networkx.algorithms.traversal.edgedfs.edge_dfs`
    :func:`~networkx.algorithms.traversal.breadth_first_search.bfs_tree`
    """
    T = nx.DiGraph()
    if source is None:
        T.add_nodes_from(G)
    else:
        T.add_node(source)
    T.add_edges_from(dfs_edges(G, source, depth_limit, sort_neighbors=sort_neighbors))
    return T

