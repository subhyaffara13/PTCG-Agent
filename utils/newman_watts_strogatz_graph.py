
def newman_watts_strogatz_graph(n, k, p, seed=None, *, create_using=None):
    """Returns a Newman–Watts–Strogatz small-world graph.

    Parameters
    ----------
    n : int
        The number of nodes.
    k : int
        Each node is joined with its `k` nearest neighbors in a ring
        topology.
    p : float
        The probability of adding a new edge for each edge.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    create_using : Graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
        Multigraph and directed types are not supported and raise a ``NetworkXError``.

    Notes
    -----
    First create a ring over $n$ nodes [1]_.  Then each node in the ring is
    connected with its $k$ nearest neighbors (or $k - 1$ neighbors if $k$
    is odd).  Then shortcuts are created by adding new edges as follows: for
    each edge $(u, v)$ in the underlying "$n$-ring with $k$ nearest
    neighbors" with probability $p$ add a new edge $(u, w)$ with
    randomly-chosen existing node $w$.  In contrast with
    :func:`watts_strogatz_graph`, no edges are removed.

    See Also
    --------
    watts_strogatz_graph

    References
    ----------
    .. [1] M. E. J. Newman and D. J. Watts,
       Renormalization group analysis of the small-world network model,
       Physics Letters A, 263, 341, 1999.
       https://doi.org/10.1016/S0375-9601(99)00757-4
    """
    create_using = check_create_using(create_using, directed=False, multigraph=False)
    if k > n:
        raise nx.NetworkXError("k>=n, choose smaller k or larger n")

    # If k == n the graph return is a complete graph
    if k == n:
        return nx.complete_graph(n, create_using)

    G = empty_graph(n, create_using)
    nlist = list(G.nodes())
    fromv = nlist
    # connect the k/2 neighbors
    for j in range(1, k // 2 + 1):
        tov = fromv[j:] + fromv[0:j]  # the first j are now last
        for i in range(len(fromv)):
            G.add_edge(fromv[i], tov[i])
    # for each edge u-v, with probability p, randomly select existing
    # node w and add new edge u-w
    e = list(G.edges())
    for u, v in e:
        if seed.random() < p:
            w = seed.choice(nlist)
            # no self-loops and reject if edge u-w exists
            # is that the correct NWS model?
            while w == u or G.has_edge(u, w):
                w = seed.choice(nlist)
                if G.degree(u) >= n - 1:
                    break  # skip this rewiring
            else:
                G.add_edge(u, w)
    return G

