
def tadpole_graph(m, n, create_using=None):
    """Returns the (m,n)-tadpole graph; ``C_m`` connected to ``P_n``.

    This graph on m+n nodes connects a cycle of size `m` to a path of length `n`.
    It looks like a tadpole. It is also called a kite graph or a dragon graph.

    .. plot::

        >>> nx.draw(nx.tadpole_graph(3, 5))

    Parameters
    ----------
    m, n : int or iterable container of nodes
        If an integer, nodes are from ``range(m)`` and ``range(m,m+n)``.
        If a container of nodes, those nodes appear in the graph.
        Warning: `m` and `n` are not checked for duplicates and if present the
        resulting graph may not be as desired.

        The nodes for `m` appear in the cycle graph $C_m$ and the nodes
        for `n` appear in the path $P_n$.
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    Networkx graph
       A cycle of size `m` connected to a path of length `n`.

    Raises
    ------
    NetworkXError
        If ``m < 2``. The tadpole graph is undefined for ``m<2``.

    Notes
    -----
    The 2 subgraphs are joined via an edge ``(m-1, m)``.
    If ``n=0``, this is a cycle graph.
    `m` and/or `n` can be a container of nodes instead of an integer.

    """
    m, m_nodes = m
    M = len(m_nodes)
    if M < 2:
        raise NetworkXError("Invalid description: m should indicate at least 2 nodes")

    n, n_nodes = n
    if isinstance(m, numbers.Integral) and isinstance(n, numbers.Integral):
        n_nodes = list(range(M, M + n))

    # the circle
    G = cycle_graph(m_nodes, create_using)
    if G.is_directed():
        raise NetworkXError("Directed Graph not supported")

    # the stick
    nx.add_path(G, [m_nodes[-1]] + list(n_nodes))

    return G

