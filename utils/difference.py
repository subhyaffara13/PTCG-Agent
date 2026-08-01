
def difference(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """
    Returns the absolute value of the pixel-by-pixel difference between the two
    images. ::

        out = abs(image1 - image2)

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image1.load()
    image2.load()
    return image1._new(image1.im.chop_difference(image2.im))


def difference(iterable, func=sub, *, initial=None):
    """This function is the inverse of :func:`itertools.accumulate`. By default
    it will compute the first difference of *iterable* using
    :func:`operator.sub`:

        >>> from itertools import accumulate
        >>> iterable = accumulate([0, 1, 2, 3, 4])  # produces 0, 1, 3, 6, 10
        >>> list(difference(iterable))
        [0, 1, 2, 3, 4]

    *func* defaults to :func:`operator.sub`, but other functions can be
    specified. They will be applied as follows::

        A, B, C, D, ... --> A, func(B, A), func(C, B), func(D, C), ...

    For example, to do progressive division:

        >>> iterable = [1, 2, 6, 24, 120]
        >>> func = lambda x, y: x // y
        >>> list(difference(iterable, func))
        [1, 2, 3, 4, 5]

    If the *initial* keyword is set, the first element will be skipped when
    computing successive differences.

        >>> it = [10, 11, 13, 16]  # from accumulate([1, 2, 3], initial=10)
        >>> list(difference(it, initial=10))
        [1, 2, 3]

    """
    a, b = tee(iterable)
    try:
        first = [next(b)]
    except StopIteration:
        return iter([])

    if initial is not None:
        first = []

    return chain(first, map(func, b, a))


def difference(G, H):
    """Returns a new graph that contains the edges that exist in G but not in H.

    The node sets of H and G must be the same.

    Parameters
    ----------
    G,H : graph
       A NetworkX graph. G and H must have the same node sets.

    Returns
    -------
    D : A new graph with the same type as G.

    Notes
    -----
    Attributes from the graph, nodes, and edges are not copied to the new
    graph.  If you want a new graph of the difference of G and H with
    the attributes (including edge data) from G use remove_nodes_from()
    as follows:

    >>> G = nx.path_graph(3)
    >>> H = nx.path_graph(5)
    >>> R = G.copy()
    >>> R.remove_nodes_from(n for n in G if n in H)

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (1, 2), (1, 3)])
    >>> H = nx.Graph([(0, 1), (1, 2), (0, 3)])
    >>> R = nx.difference(G, H)
    >>> R.nodes
    NodeView((0, 1, 2, 3))
    >>> R.edges
    EdgeView([(0, 2), (1, 3)])
    """
    # create new graph
    if not G.is_multigraph() == H.is_multigraph():
        raise nx.NetworkXError("G and H must both be graphs or multigraphs.")
    R = nx.create_empty_copy(G, with_data=False)

    if set(G) != set(H):
        raise nx.NetworkXError("Node sets of graphs not equal")

    if G.is_multigraph():
        edges = G.edges(keys=True)
    else:
        edges = G.edges()
    for e in edges:
        if not H.has_edge(*e):
            R.add_edge(*e)
    return R


def difference(ctx, s, n):
    r"""
    Given a sequence `(s_k)` containing at least `n+1` items, returns the
    `n`-th forward difference,

    .. math ::

        \Delta^n = \sum_{k=0}^{\infty} (-1)^{k+n} {n \choose k} s_k.
    """
    n = int(n)
    d = ctx.zero
    b = (-1) ** (n & 1)
    for k in xrange(n+1):
        d += b * s[k]
        b = (b * (k-n)) // (k+1)
    return d

