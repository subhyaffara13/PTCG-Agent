
def fast_gnp_random_graph(n, p, seed=None, directed=False, *, create_using=None):
    """Returns a $G_{n,p}$ random graph, also known as an Erdős-Rényi graph or
    a binomial graph.

    Parameters
    ----------
    n : int
        The number of nodes.
    p : float
        Probability for edge creation.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    directed : bool, optional (default=False)
        If True, this function returns a directed graph.
    create_using : Graph constructor, optional (default=nx.Graph or nx.DiGraph)
        Graph type to create. If graph instance, then cleared before populated.
        Multigraph types are not supported and raise a ``NetworkXError``.
        By default NetworkX Graph or DiGraph are used depending on `directed`.

    Notes
    -----
    The $G_{n,p}$ graph algorithm chooses each of the $[n (n - 1)] / 2$
    (undirected) or $n (n - 1)$ (directed) possible edges with probability $p$.

    This algorithm [1]_ runs in $O(n + m)$ time, where `m` is the expected number of
    edges, which equals $p n (n - 1) / 2$. This should be faster than
    :func:`gnp_random_graph` when $p$ is small and the expected number of edges
    is small (that is, the graph is sparse).

    See Also
    --------
    gnp_random_graph

    References
    ----------
    .. [1] Vladimir Batagelj and Ulrik Brandes,
       "Efficient generation of large random networks",
       Phys. Rev. E, 71, 036113, 2005.
    """
    default = nx.DiGraph if directed else nx.Graph
    create_using = check_create_using(
        create_using, directed=directed, multigraph=False, default=default
    )
    if p <= 0 or p >= 1:
        return nx.gnp_random_graph(
            n, p, seed=seed, directed=directed, create_using=create_using
        )

    G = empty_graph(n, create_using=create_using)

    lp = math.log(1.0 - p)

    if directed:
        v = 1
        w = -1
        while v < n:
            lr = math.log(1.0 - seed.random())
            w = w + 1 + int(lr / lp)
            while w >= v and v < n:
                w = w - v
                v = v + 1
            if v < n:
                G.add_edge(w, v)

    # Nodes in graph are from 0,n-1 (start with v as the second node index).
    v = 1
    w = -1
    while v < n:
        lr = math.log(1.0 - seed.random())
        w = w + 1 + int(lr / lp)
        while w >= v and v < n:
            w = w - v
            v = v + 1
        if v < n:
            G.add_edge(v, w)
    return G

