
def gnm_random_graph(n, m, seed=None, directed=False, *, create_using=None):
    """Returns a $G_{n,m}$ random graph.

    In the $G_{n,m}$ model, a graph is chosen uniformly at random from the set
    of all graphs with $n$ nodes and $m$ edges.

    This algorithm should be faster than :func:`dense_gnm_random_graph` for
    sparse graphs.

    Parameters
    ----------
    n : int
        The number of nodes.
    m : int
        The number of edges.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    directed : bool, optional (default=False)
        If True return a directed graph
    create_using : Graph constructor, optional (default=nx.Graph or nx.DiGraph)
        Graph type to create. If graph instance, then cleared before populated.
        Multigraph types are not supported and raise a ``NetworkXError``.
        By default NetworkX Graph or DiGraph are used depending on `directed`.

    See also
    --------
    dense_gnm_random_graph

    """
    default = nx.DiGraph if directed else nx.Graph
    create_using = check_create_using(
        create_using, directed=directed, multigraph=False, default=default
    )
    if n == 1:
        return nx.empty_graph(n, create_using=create_using)
    max_edges = n * (n - 1) if directed else n * (n - 1) / 2.0
    if m >= max_edges:
        return complete_graph(n, create_using=create_using)

    G = nx.empty_graph(n, create_using=create_using)
    nlist = list(G)
    edge_count = 0
    while edge_count < m:
        # generate random edge,u,v
        u = seed.choice(nlist)
        v = seed.choice(nlist)
        if u == v or G.has_edge(u, v):
            continue
        else:
            G.add_edge(u, v)
            edge_count = edge_count + 1
    return G

