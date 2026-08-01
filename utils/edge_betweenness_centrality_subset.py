
def edge_betweenness_centrality_subset(
    G, sources, targets, normalized=False, weight=None
):
    r"""Compute betweenness centrality for edges for a subset of nodes.

    .. math::

       c_B(e) = \sum_{s \in S, t \in T} \frac{\sigma(s, t | e)}{\sigma(s, t)}

    where $S$ is the set of sources, $T$ is the set of targets,
    $\sigma(s, t)$ is the number of shortest $(s, t)$-paths,
    and $\sigma(s, t | e)$ is the number of those paths
    passing through edge $e$ [1]_.
    The denominator $\sigma(s, t)$ is a normalization factor that can be
    turned off to get the raw path counts.

    Parameters
    ----------
    G : graph
        A networkx graph.

    sources: list of nodes
        Nodes to use as sources for shortest paths in betweenness.

    targets: list of nodes
        Nodes to use as targets for shortest paths in betweenness.

    normalized : bool, optional (default=False)
        If `True`, the betweenness values are rescaled by dividing by the number of
        possible $(s, t)$-pairs in the graph.

    weight : None or string, optional (default=None)
        If `None`, all edge weights are 1.
        Otherwise holds the name of the edge attribute used as weight.
        Weights are used to calculate weighted shortest paths, so they are
        interpreted as distances.

    Returns
    -------
    edges : dict
        Dictionary of edges with betweenness centrality as the value.

    See Also
    --------
    betweenness_centrality
    betweenness_centrality_subset
    edge_betweenness_centrality
    edge_load

    Notes
    -----
    The basic algorithm is from [1]_.

    For weighted graphs the edge weights must be greater than zero.
    Zero edge weights can produce an infinite number of equal length
    paths between pairs of nodes.

    The normalization might seem a little strange but it is the same
    as in edge_betweenness_centrality() and is designed to make
    edge_betweenness_centrality(G) be the same as
    edge_betweenness_centrality_subset(G,sources=G.nodes(),targets=G.nodes()).

    References
    ----------
    .. [1] Ulrik Brandes: On Variants of Shortest-Path Betweenness
       Centrality and their Generic Computation.
       Social Networks 30(2):136-145, 2008.
       https://doi.org/10.1016/j.socnet.2007.11.001
    """
    b = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    b.update(dict.fromkeys(G.edges(), 0.0))  # b[e] for e in G.edges()
    for s in sources:
        # single source shortest paths
        if weight is None:  # use BFS
            S, P, sigma, _ = shortest_path(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma, _ = dijkstra(G, s, weight)
        b = _accumulate_edges_subset(b, S, P, sigma, s, targets)
    for n in G:  # remove nodes to only return edges
        del b[n]
    b = _rescale(b, len(G), normalized=normalized, directed=G.is_directed())
    if G.is_multigraph():
        b = _add_edge_keys(G, b, weight=weight)
    return b

