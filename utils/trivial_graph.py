
def trivial_graph(create_using=None):
    """Return the Trivial graph with one node (with label 0) and no edges.

    .. plot::

        >>> nx.draw(nx.trivial_graph(), with_labels=True)

    """
    G = empty_graph(1, create_using)
    return G

