
def path_graph(n, create_using=None):
    """Returns the Path graph `P_n` of linearly connected nodes.

    .. plot::

        >>> nx.draw(nx.path_graph(5))

    Parameters
    ----------
    n : int or iterable
        If an integer, nodes are 0 to n - 1.
        If an iterable of nodes, in the order they appear in the path.
        Warning: n is not checked for duplicates and if present the
        resulting graph may not be as desired. Make sure you have no duplicates.
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    """
    _, nodes = n
    G = empty_graph(nodes, create_using)
    G.add_edges_from(pairwise(nodes))
    return G


def path_graph():
    """Return a path graph of length three."""
    G = nx.path_graph(3, create_using=nx.DiGraph)
    G.graph["name"] = "path"
    nx.freeze(G)
    return G

