
def girth(G):
    """Returns the girth of the graph.

    The girth of a graph is the length of its shortest cycle, or infinity if
    the graph is acyclic. The algorithm follows the description given on the
    Wikipedia page [1]_, and runs in time O(mn) on a graph with m edges and n
    nodes.

    Parameters
    ----------
    G : NetworkX Graph

    Returns
    -------
    int or math.inf

    Examples
    --------
    All examples below (except P_5) can easily be checked using Wikipedia,
    which has a page for each of these famous graphs.

    >>> nx.girth(nx.chvatal_graph())
    4
    >>> nx.girth(nx.tutte_graph())
    4
    >>> nx.girth(nx.petersen_graph())
    5
    >>> nx.girth(nx.heawood_graph())
    6
    >>> nx.girth(nx.pappus_graph())
    6
    >>> nx.girth(nx.path_graph(5))
    inf

    References
    ----------
    .. [1] `Wikipedia: Girth <https://en.wikipedia.org/wiki/Girth_(graph_theory)>`_

    """
    girth = depth_limit = inf
    tree_edge = nx.algorithms.traversal.breadth_first_search.TREE_EDGE
    level_edge = nx.algorithms.traversal.breadth_first_search.LEVEL_EDGE
    for n in G:
        # run a BFS from source n, keeping track of distances; since we want
        # the shortest cycle, no need to explore beyond the current minimum length
        depth = {n: 0}
        for u, v, label in nx.bfs_labeled_edges(G, n):
            du = depth[u]
            if du > depth_limit:
                break
            if label is tree_edge:
                depth[v] = du + 1
            else:
                # if (u, v) is a level edge, the length is du + du + 1 (odd)
                # otherwise, it's a forward edge; length is du + (du + 1) + 1 (even)
                delta = label is level_edge
                length = du + du + 2 - delta
                if length < girth:
                    girth = length
                    depth_limit = du - delta

    return girth

