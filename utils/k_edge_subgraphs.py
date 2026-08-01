
def k_edge_subgraphs(G, k):
    """Generates nodes in each maximal k-edge-connected subgraph in G.

    Parameters
    ----------
    G : NetworkX graph

    k : Integer
        Desired edge connectivity

    Returns
    -------
    k_edge_subgraphs : a generator of k-edge-subgraphs
        Each k-edge-subgraph is a maximal set of nodes that defines a subgraph
        of G that is k-edge-connected.

    See Also
    --------
    :func:`edge_connectivity`
    :func:`k_edge_components` : similar to this function, but nodes only
        need to have k-edge-connectivity within the graph G and the subgraphs
        might not be k-edge-connected.

    Raises
    ------
    NetworkXNotImplemented
        If the input graph is a multigraph.

    ValueError:
        If k is less than 1

    Notes
    -----
    Attempts to use the most efficient implementation available based on k.
    If k=1, or k=2 and the graph is undirected, then this simply calls
    `k_edge_components`.  Otherwise the algorithm from _[1] is used.

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
    >>> # note this does not return {1, 4} unlike k_edge_components
    >>> sorted(map(sorted, nx.k_edge_subgraphs(G, k=3)))
    [[1], [2], [3], [4], [5, 6, 7, 8]]

    References
    ----------
    .. [1] Zhou, Liu, et al. (2012) Finding maximal k-edge-connected subgraphs
        from a large graph.  ACM International Conference on Extending Database
        Technology 2012 480-–491.
        https://openproceedings.org/2012/conf/edbt/ZhouLYLCL12.pdf
    """
    if k < 1:
        raise ValueError("k cannot be less than 1")
    if G.is_directed():
        if k <= 1:
            # For directed graphs ,
            # When k == 1, k-edge-ccs and k-edge-subgraphs are the same
            return k_edge_components(G, k)
        else:
            return _k_edge_subgraphs_nodes(G, k)
    else:
        if k <= 2:
            # For undirected graphs,
            # when k <= 2, k-edge-ccs and k-edge-subgraphs are the same
            return k_edge_components(G, k)
        else:
            return _k_edge_subgraphs_nodes(G, k)

