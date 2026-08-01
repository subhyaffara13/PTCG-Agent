
def edge_betweenness_centrality(G, k=None, normalized=True, weight=None, seed=None):
    r"""Compute betweenness centrality for edges.

    Betweenness centrality of an edge $e$ is the sum of the
    fraction of all-pairs shortest paths that pass through $e$.

    .. math::

       c_B(e) = \sum_{s, t \in V} \frac{\sigma(s, t | e)}{\sigma(s, t)}

    where $V$ is the set of nodes, $\sigma(s, t)$ is the number of
    shortest $(s, t)$-paths, and $\sigma(s, t | e)$ is the number of
    those paths passing through edge $e$ [1]_.
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

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
        Note that this is only used if ``k is not None``.

    Returns
    -------
    edges : dict
        Dictionary of edges with betweenness centrality as the value.

    See Also
    --------
    betweenness_centrality
    edge_betweenness_centrality_subset
    edge_load

    Notes
    -----
    The algorithm is from Ulrik Brandes [1]_.

    For weighted graphs the edge weights must be greater than zero.
    Zero edge weights can produce an infinite number of equal length
    paths between pairs of nodes.

    References
    ----------
    .. [1] Ulrik Brandes: On Variants of Shortest-Path Betweenness
       Centrality and their Generic Computation.
       Social Networks 30(2):136--145, 2008.
       https://doi.org/10.1016/j.socnet.2007.11.001

    Examples
    --------
    Consider an undirected 3-path. Each pair of nodes has exactly one shortest
    path between them. Since the graph is undirected, only ordered pairs are counted.
    Each edge has two shortest paths passing through it.
    As such, the raw counts should be ``{(0, 1): 2, (1, 2): 2}``.

    >>> G = nx.path_graph(3)
    >>> nx.edge_betweenness_centrality(G, normalized=False)
    {(0, 1): 2.0, (1, 2): 2.0}

    With normalization, the values are divided by the number of ordered $(s, t)$-pairs,
    which is $n(n-1)/2$. For the 3-path, this is $3(3-1)/2 = 3$.

    >>> nx.edge_betweenness_centrality(G, normalized=True)
    {(0, 1): 0.6666666666666666, (1, 2): 0.6666666666666666}

    For a directed graph, all $(s, t)$-pairs are considered. The normalization factor
    is $n(n-1)$ to reflect this.

    >>> DG = nx.path_graph(3, create_using=nx.DiGraph)
    >>> nx.edge_betweenness_centrality(DG, normalized=False)
    {(0, 1): 2.0, (1, 2): 2.0}
    >>> nx.edge_betweenness_centrality(DG, normalized=True)
    {(0, 1): 0.3333333333333333, (1, 2): 0.3333333333333333}

    Computing the full edge betweenness centrality can be costly.
    This function can also be used to compute approximate edge betweenness centrality
    by setting `k`. This determines the number of source nodes to sample.

    Since the partial sums only include `k` terms, instead of ``n``,
    we multiply them by ``n / k``, to approximate the full sum.
    As the sets of sources and targets are not the same anymore,
    paths have to be counted in a directed way. We thus count each as half a path.
    This ensures that the results approximate the standard betweenness for ``k == n``.

    For instance, in the undirected 3-path graph case, setting ``k = 2`` (with ``seed=42``)
    selects nodes 0 and 2 as sources.
    This means only shortest paths starting at these nodes are considered.
    The raw counts are ``{(0, 1): 3, (1, 2): 3}``. Accounting for the partial sum
    and applying the undirectedness half-path correction, we get

    >>> nx.edge_betweenness_centrality(G, k=2, normalized=False, seed=42)
    {(0, 1): 2.25, (1, 2): 2.25}

    When normalizing, we instead want to divide by the total number of $(s, t)$-pairs.
    This is $k(n-1)$, which is $4$ in our case.

    >>> nx.edge_betweenness_centrality(G, k=2, normalized=True, seed=42)
    {(0, 1): 0.75, (1, 2): 0.75}
    """
    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    # b[e]=0 for e in G.edges()
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
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
        betweenness = _accumulate_edges(betweenness, S, P, sigma, s)
    # rescaling
    for n in G:  # remove nodes to only return edges
        del betweenness[n]
    betweenness = _rescale(
        betweenness,
        len(G),
        normalized=normalized,
        directed=G.is_directed(),
        sampled_nodes=None if k is None else nodes,
    )
    if G.is_multigraph():
        betweenness = _add_edge_keys(G, betweenness, weight=weight)
    return betweenness

