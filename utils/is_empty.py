
def is_empty(G):
    """Returns True if `G` has no edges.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    Returns
    -------
    bool
        True if `G` has no edges, and False otherwise.

    Notes
    -----
    An empty graph can have nodes but not edges. The empty graph with zero
    nodes is known as the null graph. This is an $O(n)$ operation where n
    is the number of nodes in the graph.

    """
    return not any(G._adj.values())

