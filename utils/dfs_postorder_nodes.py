
def dfs_postorder_nodes(G, source=None, depth_limit=None, *, sort_neighbors=None):
    """Generate nodes in a depth-first-search post-ordering starting at source.

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
    nodes: generator
       A generator of nodes in a depth-first-search post-ordering.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> list(nx.dfs_postorder_nodes(G, source=0))
    [4, 3, 2, 1, 0]
    >>> list(nx.dfs_postorder_nodes(G, source=0, depth_limit=2))
    [1, 0]

    Notes
    -----
    If a source is not specified then a source is chosen arbitrarily and
    repeatedly until all components in the graph are searched.

    The implementation of this function is adapted from David Eppstein's
    depth-first search function in `PADS`_, with modifications
    to allow depth limits based on the Wikipedia article
    "`Depth-limited search`_".

    .. _PADS: http://www.ics.uci.edu/~eppstein/PADS
    .. _Depth-limited search: https://en.wikipedia.org/wiki/Depth-limited_search

    See Also
    --------
    dfs_edges
    dfs_preorder_nodes
    dfs_labeled_edges
    :func:`~networkx.algorithms.traversal.edgedfs.edge_dfs`
    :func:`~networkx.algorithms.traversal.breadth_first_search.bfs_tree`
    """
    edges = nx.dfs_labeled_edges(
        G, source=source, depth_limit=depth_limit, sort_neighbors=sort_neighbors
    )
    return (v for u, v, d in edges if d == "reverse")

