
def star_graph(n, create_using=None):
    """Return a star graph.

    The star graph consists of one center node connected to `n` outer nodes.

    .. plot::

        >>> nx.draw(nx.star_graph(6))

    Parameters
    ----------
    n : int or iterable
        If an integer, node labels are ``0`` to `n`, with center ``0``.
        If an iterable of nodes, the center is the first.
        Warning: `n` is not checked for duplicates and if present, the
        resulting graph may not be as desired. Make sure you have no duplicates.
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Examples
    --------
    A star graph with 3 spokes can be generated with

    >>> G = nx.star_graph(3)
    >>> sorted(G.edges)
    [(0, 1), (0, 2), (0, 3)]

    For directed graphs, the convention is to have edges pointing from the hub
    to the spokes:

    >>> DG1 = nx.star_graph(3, create_using=nx.DiGraph)
    >>> sorted(DG1.edges)
    [(0, 1), (0, 2), (0, 3)]

    Other possible definitions have edges pointing from the spokes to the hub:

    >>> DG2 = nx.star_graph(3, create_using=nx.DiGraph).reverse()
    >>> sorted(DG2.edges)
    [(1, 0), (2, 0), (3, 0)]

    or have bidirectional edges:

    >>> DG3 = nx.star_graph(3).to_directed()
    >>> sorted(DG3.edges)
    [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)]

    Notes
    -----
    The graph has ``n + 1`` nodes for integer `n`.
    So ``star_graph(3)`` is the same as ``star_graph(range(4))``.
    """
    n, nodes = n
    if isinstance(n, numbers.Integral):
        nodes.append(int(n))  # There should be n + 1 nodes.
    G = empty_graph(nodes, create_using)

    if len(nodes) > 1:
        hub, *spokes = nodes
        G.add_edges_from((hub, node) for node in spokes)
    return G

