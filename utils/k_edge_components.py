
def k_edge_components(G, k):
    """Generates nodes in each maximal k-edge-connected component in G.

    Parameters
    ----------
    G : NetworkX graph

    k : Integer
        Desired edge connectivity

    Returns
    -------
    k_edge_components : a generator of k-edge-ccs. Each set of returned nodes
       will have k-edge-connectivity in the graph G.

    See Also
    --------
    :func:`local_edge_connectivity`
    :func:`k_edge_subgraphs` : similar to this function, but the subgraph
        defined by the nodes must also have k-edge-connectivity.
    :func:`k_components` : similar to this function, but uses node-connectivity
        instead of edge-connectivity

    Raises
    ------
    NetworkXNotImplemented
        If the input graph is a multigraph.

    ValueError:
        If k is less than 1

    Notes
    -----
    Attempts to use the most efficient implementation available based on k.
    If k=1, this is simply connected components for directed graphs and
    connected components for undirected graphs.
    If k=2 on an efficient bridge connected component algorithm from _[1] is
    run based on the chain decomposition.
    Otherwise, the algorithm from _[2] is used.

    Examples
    --------
    >>> import itertools as it
    >>> from networkx.utils import pairwise
    >>> paths = [
    ...     (1, 2, 4, 3, 1, 4),
    ...     (5, 6, 7, 8, 5, 7, 8, 6),
    ... ]
    >>> G = nx.Graph()
    >>> G.add_nodes_from(it.chain(*paths))
    >>> G.add_edges_from(it.chain(*[pairwise(path) for path in paths]))
    >>> # note this returns {1, 4} unlike k_edge_subgraphs
    >>> sorted(map(sorted, nx.k_edge_components(G, k=3)))
    [[1, 4], [2], [3], [5, 6, 7, 8]]

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Bridge_%28graph_theory%29
    .. [2] Wang, Tianhao, et al. (2015) A simple algorithm for finding all
        k-edge-connected components.
        http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0136264
    """
    # Compute k-edge-ccs using the most efficient algorithms available.
    if k < 1:
        raise ValueError("k cannot be less than 1")
    if G.is_directed():
        if k == 1:
            return nx.strongly_connected_components(G)
        else:
            # TODO: investigate https://arxiv.org/abs/1412.6466 for k=2
            aux_graph = EdgeComponentAuxGraph.construct(G)
            return aux_graph.k_edge_components(k)
    else:
        if k == 1:
            return nx.connected_components(G)
        elif k == 2:
            return bridge_components(G)
        else:
            aux_graph = EdgeComponentAuxGraph.construct(G)
            return aux_graph.k_edge_components(k)

