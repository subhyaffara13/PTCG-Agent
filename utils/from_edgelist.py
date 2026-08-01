
def from_edgelist(edgelist, create_using=None):
    """Returns a graph from a list of edges.

    Parameters
    ----------
    edgelist : list or iterator
      Edge tuples

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.

    Examples
    --------
    >>> edgelist = [(0, 1)]  # single edge (0,1)
    >>> G = nx.from_edgelist(edgelist)

    or

    >>> G = nx.Graph(edgelist)  # use Graph constructor

    """
    G = nx.empty_graph(0, create_using)
    G.add_edges_from(edgelist)
    return G

