
def dorogovtsev_goltsev_mendes_graph(n, create_using=None):
    """Returns the hierarchically constructed Dorogovtsev--Goltsev--Mendes graph.

    The Dorogovtsev--Goltsev--Mendes [1]_ procedure deterministically produces a
    scale-free graph with ``3/2 * (3**(n-1) + 1)`` nodes
    and ``3**n`` edges for a given `n`.

    Note that `n` denotes the number of times the state transition is applied,
    starting from the base graph with ``n = 0`` (no transitions), as in [2]_.
    This is different from the parameter ``t = n - 1`` in [1]_.

    .. plot::

        >>> nx.draw(nx.dorogovtsev_goltsev_mendes_graph(3))

    Parameters
    ----------
    n : integer
        The generation number.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. Directed graphs and multigraphs are not supported.

    Returns
    -------
    G : NetworkX `Graph`

    Raises
    ------
    NetworkXError
        If `n` is less than zero.

        If `create_using` is a directed graph or multigraph.

    Examples
    --------
    >>> G = nx.dorogovtsev_goltsev_mendes_graph(3)
    >>> G.number_of_nodes()
    15
    >>> G.number_of_edges()
    27
    >>> nx.is_planar(G)
    True

    References
    ----------
    .. [1] S. N. Dorogovtsev, A. V. Goltsev and J. F. F. Mendes,
        "Pseudofractal scale-free web", Physical Review E 65, 066122, 2002.
        https://arxiv.org/pdf/cond-mat/0112143.pdf
    .. [2] Weisstein, Eric W. "Dorogovtsev--Goltsev--Mendes Graph".
        From MathWorld--A Wolfram Web Resource.
        https://mathworld.wolfram.com/Dorogovtsev-Goltsev-MendesGraph.html
    """
    if n < 0:
        raise NetworkXError("n must be greater than or equal to 0")

    G = empty_graph(0, create_using)
    if G.is_directed():
        raise NetworkXError("directed graph not supported")
    if G.is_multigraph():
        raise NetworkXError("multigraph not supported")

    G.add_edge(0, 1)
    new_node = 2  # next node to be added
    for _ in range(n):  # iterate over number of generations.
        new_edges = []
        for u, v in G.edges():
            new_edges.append((u, new_node))
            new_edges.append((v, new_node))
            new_node += 1

        G.add_edges_from(new_edges)
    return G

