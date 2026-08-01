
def generic_bfs_edges(G, source, neighbors=None, depth_limit=None):
    """Iterate over edges in a breadth-first search.

    The breadth-first search begins at `source` and enqueues the
    neighbors of newly visited nodes specified by the `neighbors`
    function.

    Parameters
    ----------
    G : NetworkX graph

    source : node
        Starting node for the breadth-first search; this function
        iterates over only those edges in the component reachable from
        this node.

    neighbors : function
        A function that takes a newly visited node of the graph as input
        and returns an *iterator* (not just a list) of nodes that are
        neighbors of that node with custom ordering. If not specified, this is
        just the ``G.neighbors`` method, but in general it can be any function
        that returns an iterator over some or all of the neighbors of a
        given node, in any order.

    depth_limit : int, optional(default=len(G))
        Specify the maximum search depth.

    Yields
    ------
    edge
        Edges in the breadth-first search starting from `source`.

    Examples
    --------
    >>> G = nx.path_graph(7)
    >>> list(nx.generic_bfs_edges(G, source=0))
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
    >>> list(nx.generic_bfs_edges(G, source=2))
    [(2, 1), (2, 3), (1, 0), (3, 4), (4, 5), (5, 6)]
    >>> list(nx.generic_bfs_edges(G, source=2, depth_limit=2))
    [(2, 1), (2, 3), (1, 0), (3, 4)]

    The `neighbors` param can be used to specify the visitation order of each
    node's neighbors generically. In the following example, we modify the default
    neighbor to return *odd* nodes first:

    >>> def odd_first(n):
    ...     return sorted(G.neighbors(n), key=lambda x: x % 2, reverse=True)

    >>> G = nx.star_graph(5)
    >>> list(nx.generic_bfs_edges(G, source=0))  # Default neighbor ordering
    [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
    >>> list(nx.generic_bfs_edges(G, source=0, neighbors=odd_first))
    [(0, 1), (0, 3), (0, 5), (0, 2), (0, 4)]

    Notes
    -----
    This implementation is from `PADS`_, which was in the public domain
    when it was first accessed in July, 2004.  The modifications
    to allow depth limits are based on the Wikipedia article
    "`Depth-limited-search`_".

    .. _PADS: http://www.ics.uci.edu/~eppstein/PADS/BFS.py
    .. _Depth-limited-search: https://en.wikipedia.org/wiki/Depth-limited_search
    """
    if neighbors is None:
        neighbors = G.neighbors
    if depth_limit is None:
        depth_limit = len(G)

    seen = {source}
    n = len(G)
    depth = 0
    next_parents_children = [(source, neighbors(source))]
    while next_parents_children and depth < depth_limit:
        this_parents_children = next_parents_children
        next_parents_children = []
        for parent, children in this_parents_children:
            for child in children:
                if child not in seen:
                    seen.add(child)
                    next_parents_children.append((child, neighbors(child)))
                    yield parent, child
            if len(seen) == n:
                return
        depth += 1

