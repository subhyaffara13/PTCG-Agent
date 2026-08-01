
def lollipop_graph(m, n, create_using=None):
    """Returns the Lollipop Graph; ``K_m`` connected to ``P_n``.

    This is the Barbell Graph without the right barbell.

    .. plot::

        >>> nx.draw(nx.lollipop_graph(3, 4))

    Parameters
    ----------
    m, n : int or iterable container of nodes
        If an integer, nodes are from ``range(m)`` and ``range(m, m+n)``.
        If a container of nodes, those nodes appear in the graph.
        Warning: `m` and `n` are not checked for duplicates and if present the
        resulting graph may not be as desired. Make sure you have no duplicates.

        The nodes for `m` appear in the complete graph $K_m$ and the nodes
        for `n` appear in the path $P_n$
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    Networkx graph
       A complete graph with `m` nodes connected to a path of length `n`.

    Notes
    -----
    The 2 subgraphs are joined via an edge ``(m-1, m)``.
    If ``n=0``, this is merely a complete graph.

    (This graph is an extremal example in David Aldous and Jim
    Fill's etext on Random Walks on Graphs.)

    """
    m, m_nodes = m
    M = len(m_nodes)
    if M < 2:
        raise NetworkXError("Invalid description: m should indicate at least 2 nodes")

    n, n_nodes = n
    if isinstance(m, numbers.Integral) and isinstance(n, numbers.Integral):
        n_nodes = list(range(M, M + n))
    N = len(n_nodes)

    # the ball
    G = complete_graph(m_nodes, create_using)
    if G.is_directed():
        raise NetworkXError("Directed Graph not supported")

    # the stick
    G.add_nodes_from(n_nodes)
    if N > 1:
        G.add_edges_from(pairwise(n_nodes))

    if len(G) != M + N:
        raise NetworkXError("Nodes must be distinct in containers m and n")

    # connect ball to stick
    if M > 0 and N > 0:
        G.add_edge(m_nodes[-1], n_nodes[0])
    return G

