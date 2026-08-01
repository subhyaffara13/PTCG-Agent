
def betweenness_centrality(G, nodes):
    r"""Compute betweenness centrality for nodes in a bipartite network.

    Betweenness centrality of a node `v` is the sum of the
    fraction of all-pairs shortest paths that pass through `v`.

    Values of betweenness are normalized by the maximum possible
    value which for bipartite graphs is limited by the relative size
    of the two node sets [1]_.

    Let `n` be the number of nodes in the node set `U` and
    `m` be the number of nodes in the node set `V`, then
    nodes in `U` are normalized by dividing by

    .. math::

       \frac{1}{2} [m^2 (s + 1)^2 + m (s + 1)(2t - s - 1) - t (2s - t + 3)] ,

    where

    .. math::

        s = (n - 1) \div m , t = (n - 1) \mod m ,

    and nodes in `V` are normalized by dividing by

    .. math::

        \frac{1}{2} [n^2 (p + 1)^2 + n (p + 1)(2r - p - 1) - r (2p - r + 3)] ,

    where,

    .. math::

        p = (m - 1) \div n , r = (m - 1) \mod n .

    Parameters
    ----------
    G : graph
        A bipartite graph

    nodes : list or container
        Container with all nodes in one bipartite node set.

    Returns
    -------
    betweenness : dictionary
        Dictionary keyed by node with bipartite betweenness centrality
        as the value.

    Examples
    --------
    >>> G = nx.cycle_graph(4)
    >>> top_nodes = {1, 2}
    >>> nx.bipartite.betweenness_centrality(G, nodes=top_nodes)
    {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25}

    See Also
    --------
    degree_centrality
    closeness_centrality
    :func:`~networkx.algorithms.bipartite.basic.sets`
    :func:`~networkx.algorithms.bipartite.basic.is_bipartite`

    Notes
    -----
    The nodes input parameter must contain all nodes in one bipartite node set,
    but the dictionary returned contains all nodes from both node sets.
    See :mod:`bipartite documentation <networkx.algorithms.bipartite>`
    for further details on how bipartite graphs are handled in NetworkX.


    References
    ----------
    .. [1] Borgatti, S.P. and Halgin, D. In press. "Analyzing Affiliation
        Networks". In Carrington, P. and Scott, J. (eds) The Sage Handbook
        of Social Network Analysis. Sage Publications.
        https://dx.doi.org/10.4135/9781446294413.n28
    """
    top = set(nodes)
    bottom = set(G) - top
    n = len(top)
    m = len(bottom)
    s, t = divmod(n - 1, m)
    bet_max_top = (
        ((m**2) * ((s + 1) ** 2))
        + (m * (s + 1) * (2 * t - s - 1))
        - (t * ((2 * s) - t + 3))
    ) / 2.0
    p, r = divmod(m - 1, n)
    bet_max_bot = (
        ((n**2) * ((p + 1) ** 2))
        + (n * (p + 1) * (2 * r - p - 1))
        - (r * ((2 * p) - r + 3))
    ) / 2.0
    betweenness = nx.betweenness_centrality(G, normalized=False, weight=None)
    for node in top:
        betweenness[node] /= bet_max_top
    for node in bottom:
        betweenness[node] /= bet_max_bot
    return betweenness


def betweenness_centrality(
    G, k=None, normalized=True, weight=None, endpoints=False, seed=None
):
    r"""Compute the shortest-path betweenness centrality for nodes.

    Betweenness centrality of a node $v$ is the sum of the
    fraction of all-pairs shortest paths that pass through $v$.

    .. math::

       c_B(v) = \sum_{s, t \in V} \frac{\sigma(s, t | v)}{\sigma(s, t)}

    where $V$ is the set of nodes, $\sigma(s, t)$ is the number of
    shortest $(s, t)$-paths, and $\sigma(s, t | v)$ is the number of
    those paths passing through some node $v$ other than $s$ and $t$.
    If $s = t$, $\sigma(s, t) = 1$, and if $v \in \{s, t\}$,
    $\sigma(s, t | v) = 0$ [2]_.
    The denominator $\sigma(s, t)$ is a normalization factor that can be
    turned off to get the raw path counts.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    k : int, optional (default=None)
        If `k` is not `None`, use `k` sampled nodes as sources for the considered paths.
        The resulting sampled counts are then inflated to approximate betweenness.
        Higher values of `k` give better approximation. Must have ``k <= len(G)``.

    normalized : bool, optional (default=True)
        If `True`, the betweenness values are rescaled by dividing by the number of
        possible $(s, t)$-pairs in the graph.

    weight : None or string, optional (default=None)
        If `None`, all edge weights are 1.
        Otherwise holds the name of the edge attribute used as weight.
        Weights are used to calculate weighted shortest paths, so they are
        interpreted as distances.

    endpoints : bool, optional (default=False)
        If `True`, include the endpoints $s$ and $t$ in the shortest path counts.
        This is taken into account when rescaling the values.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
        Note that this is only used if ``k is not None``.

    Returns
    -------
    nodes : dict
        Dictionary of nodes with betweenness centrality as the value.

    See Also
    --------
    betweenness_centrality_subset
    edge_betweenness_centrality
    load_centrality

    Notes
    -----
    The algorithm is from Ulrik Brandes [1]_.
    See [4]_ for the original first published version and [2]_ for details on
    algorithms for variations and related metrics.

    For approximate betweenness calculations, set `k` to the number of sampled
    nodes ("pivots") used as sources to estimate the betweenness values.
    The formula then sums over $s$ is in these pivots, instead of over all nodes.
    The resulting sum is then inflated to approximate the full sum.
    For a discussion of how to choose `k` for efficiency, see [3]_.

    For weighted graphs the edge weights must be greater than zero.
    Zero edge weights can produce an infinite number of equal length
    paths between pairs of nodes.

    Directed graphs and undirected graphs count paths differently.
    In directed graphs, each pair of source-target nodes is considered separately
    in each direction, as the shortest paths can differ by direction.
    However, in undirected graphs, each pair of nodes is considered only once,
    as the shortest paths are symmetric.
    This means the normalization factor to divide by is $N(N-1)$ for directed graphs
    and $N(N-1)/2$ for undirected graphs, where $N = n$ (the number of nodes)
    if endpoints are included and $N = n-1$ otherwise.

    This algorithm is not guaranteed to be correct if edge weights
    are floating point numbers. As a workaround you can use integer
    numbers by multiplying the relevant edge attributes by a convenient
    constant factor (e.g. 100) and converting to integers.

    References
    ----------
    .. [1] Ulrik Brandes:
       A Faster Algorithm for Betweenness Centrality.
       Journal of Mathematical Sociology 25(2):163--177, 2001.
       https://doi.org/10.1080/0022250X.2001.9990249
    .. [2] Ulrik Brandes:
       On Variants of Shortest-Path Betweenness
       Centrality and their Generic Computation.
       Social Networks 30(2):136--145, 2008.
       https://doi.org/10.1016/j.socnet.2007.11.001
    .. [3] Ulrik Brandes and Christian Pich:
       Centrality Estimation in Large Networks.
       International Journal of Bifurcation and Chaos 17(7):2303--2318, 2007.
       https://dx.doi.org/10.1142/S0218127407018403
    .. [4] Linton C. Freeman:
       A set of measures of centrality based on betweenness.
       Sociometry 40: 35--41, 1977
       https://doi.org/10.2307/3033543

    Examples
    --------
    Consider an undirected 3-path. Each pair of nodes has exactly one shortest
    path between them. Since the graph is undirected, only ordered pairs are counted.
    Of these (and when `endpoints` is `False`), none of the shortest paths pass
    through 0 and 2, and only the shortest path between 0 and 2 passes through 1.
    As such, the counts should be ``{0: 0, 1: 1, 2: 0}``.

    >>> G = nx.path_graph(3)
    >>> nx.betweenness_centrality(G, normalized=False, endpoints=False)
    {0: 0.0, 1: 1.0, 2: 0.0}

    If `endpoints` is `True`, we also need to count endpoints as being on the path:
    $\sigma(s, t | s) = \sigma(s, t | t) = \sigma(s, t)$.
    In our example, 0 is then part of two shortest paths (0 to 1 and 0 to 2);
    similarly, 2 is part of two shortest paths (0 to 2 and 1 to 2).
    1 is part of all three shortest paths. This makes the new raw
    counts ``{0: 2, 1: 3, 2: 2}``.

    >>> nx.betweenness_centrality(G, normalized=False, endpoints=True)
    {0: 2.0, 1: 3.0, 2: 2.0}

    With normalization, the values are divided by the number of ordered $(s, t)$-pairs.
    If we are not counting endpoints, there are $n - 1$ possible choices for $s$
    (all except the node we are computing betweenness centrality for), which in turn
    leaves $n - 2$ possible choices for $t$ as $s \ne t$.
    The total number of ordered pairs when `endpoints` is `False` is $(n - 1)(n - 2)/2 = 1$.
    If `endpoints` is `True`, there are $n(n - 1)/2 = 3$ ordered $(s, t)$-pairs to divide by.

    >>> nx.betweenness_centrality(G, normalized=True, endpoints=False)
    {0: 0.0, 1: 1.0, 2: 0.0}
    >>> nx.betweenness_centrality(G, normalized=True, endpoints=True)
    {0: 0.6666666666666666, 1: 1.0, 2: 0.6666666666666666}

    If the graph is directed instead, we now need to consider $(s, t)$-pairs
    in both directions. Our example becomes a directed 3-path.
    Without counting endpoints, we only have one path through 1 (0 to 2).
    This means the raw counts are ``{0: 0, 1: 1, 2: 0}``.

    >>> DG = nx.path_graph(3, create_using=nx.DiGraph)
    >>> nx.betweenness_centrality(DG, normalized=False, endpoints=False)
    {0: 0.0, 1: 1.0, 2: 0.0}

    If we do include endpoints, the raw counts are ``{0: 2, 1: 3, 2: 2}``.

    >>> nx.betweenness_centrality(DG, normalized=False, endpoints=True)
    {0: 2.0, 1: 3.0, 2: 2.0}

    If we want to normalize directed betweenness centrality, the raw counts
    are normalized by the number of $(s, t)$-pairs. There are $n(n - 1)$
    possible paths with endpoints and $(n - 1)(n - 2)$ without endpoints.
    In our example, that's 6 with endpoints and 2 without endpoints.

    >>> nx.betweenness_centrality(DG, normalized=True, endpoints=True)
    {0: 0.3333333333333333, 1: 0.5, 2: 0.3333333333333333}
    >>> nx.betweenness_centrality(DG, normalized=True, endpoints=False)
    {0: 0.0, 1: 0.5, 2: 0.0}

    Computing the full betweenness centrality can be costly.
    This function can also be used to compute approximate betweenness centrality
    by setting `k`. This only determines the number of source nodes to sample;
    all nodes are targets.

    For simplicity, we only consider the case where endpoints are included in the counts.
    Since the partial sums only include `k` terms, instead of ``n``,
    we multiply them by ``n / k``, to approximate the full sum.
    As the sets of sources and targets are not the same anymore,
    paths have to be counted in a directed way. We thus count each as half a path.
    This ensures that the results approximate the standard betweenness for ``k == n``.

    For instance, in the undirected 3-path graph case, setting ``k = 2`` (with ``seed=42``)
    selects nodes 0 and 2 as sources.
    This means only shortest paths starting at these nodes are considered.
    The raw counts with endpoints are ``{0: 3, 1: 4, 2: 3}``. Accounting for the partial sum
    and applying the undirectedness half-path correction, we get

    >>> nx.betweenness_centrality(G, k=2, normalized=False, endpoints=True, seed=42)
    {0: 2.25, 1: 3.0, 2: 2.25}

    When normalizing, we instead want to divide by the total number of $(s, t)$-pairs.
    This is $k(n - 1)$ with endpoints.

    >>> nx.betweenness_centrality(G, k=2, normalized=True, endpoints=True, seed=42)
    {0: 0.75, 1: 1.0, 2: 0.75}
    """
    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    if k == len(G):
        # This is done for performance; the result is the same regardless.
        k = None
    if k is None:
        nodes = G
    else:
        nodes = seed.sample(list(G.nodes()), k)
    for s in nodes:
        # single source shortest paths
        if weight is None:  # use BFS
            S, P, sigma, _ = _single_source_shortest_path_basic(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma, _ = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        if endpoints:
            betweenness, _ = _accumulate_endpoints(betweenness, S, P, sigma, s)
        else:
            betweenness, _ = _accumulate_basic(betweenness, S, P, sigma, s)
    # rescaling
    betweenness = _rescale(
        betweenness,
        len(G),
        normalized=normalized,
        directed=G.is_directed(),
        endpoints=endpoints,
        sampled_nodes=None if k is None else nodes,
    )
    return betweenness

