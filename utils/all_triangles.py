
def all_triangles(G, nbunch=None):
    """
    Yields all unique triangles in an undirected graph.

    A triangle is a set of three distinct nodes where each node is connected to
    the other two.

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph.

    nbunch : node, iterable of nodes, or None (default=None)
        If a node or iterable of nodes, only triangles involving at least one
        node in `nbunch` are yielded.
        If ``None``, yields all unique triangles in the graph.

    Yields
    ------
    tuple
        A tuple of three nodes forming a triangle ``(u, v, w)``.

    Examples
    --------
    >>> G = nx.complete_graph(4)
    >>> sorted([sorted(t) for t in all_triangles(G)])
    [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]

    Notes
    -----
    This algorithm ensures each triangle is yielded once using an internal node ordering.
    In multigraphs, triangles are identified by their unique set of nodes,
    ignoring multiple edges between the same nodes. Self-loops are ignored.
    Runs in ``O(m * d)`` time in the worst case, where ``m`` the number of edges
    and ``d`` the maximum degree.

    See Also
    --------
    :func:`~networkx.algorithms.triads.all_triads` : related function for directed graphs
    """
    if nbunch is None:
        nbunch = relevant_nodes = G
    else:
        nbunch = dict.fromkeys(G.nbunch_iter(nbunch))
        relevant_nodes = chain(
            nbunch,
            (nbr for node in nbunch for nbr in G.neighbors(node) if nbr not in nbunch),
        )

    node_to_id = {node: i for i, node in enumerate(relevant_nodes)}

    for u in nbunch:
        u_id = node_to_id[u]
        u_nbrs = G._adj[u].keys()
        for v in u_nbrs:
            v_id = node_to_id.get(v, -1)
            if v_id <= u_id:
                continue
            v_nbrs = G._adj[v].keys()
            for w in v_nbrs & u_nbrs:
                if node_to_id.get(w, -1) > v_id:
                    yield u, v, w

