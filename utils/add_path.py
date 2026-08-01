
def add_path(G_to_add_to, nodes_for_path, **attr):
    """Add a path to the Graph G_to_add_to.

    Parameters
    ----------
    G_to_add_to : graph
        A NetworkX graph
    nodes_for_path : iterable container
        A container of nodes.  A path will be constructed from
        the nodes (in order) and added to the graph.
    attr : keyword arguments, optional (default= no attributes)
        Attributes to add to every edge in path.

    See Also
    --------
    add_star, add_cycle

    Examples
    --------
    >>> G = nx.Graph()
    >>> nx.add_path(G, [0, 1, 2, 3])
    >>> nx.add_path(G, [10, 11, 12], weight=7)
    """
    nlist = iter(nodes_for_path)
    try:
        first_node = next(nlist)
    except StopIteration:
        return
    G_to_add_to.add_node(first_node)
    G_to_add_to.add_edges_from(pairwise(chain((first_node,), nlist)), **attr)

