
def edge_subgraph(G, edges):
    """Returns a view of the subgraph induced by the specified edges.

    The induced subgraph contains each edge in `edges` and each
    node incident to any of those edges.

    Parameters
    ----------
    G : NetworkX Graph
    edges : iterable
        An iterable of edges. Edges not present in `G` are ignored.

    Returns
    -------
    subgraph : SubGraph View
        A read-only edge-induced subgraph of `G`.
        Changes to `G` are reflected in the view.

    Notes
    -----
    To create a mutable subgraph with its own copies of nodes
    edges and attributes use `subgraph.copy()` or `Graph(subgraph)`

    If you create a subgraph of a subgraph recursively you can end up
    with a chain of subgraphs that becomes very slow with about 15
    nested subgraph views. Luckily the edge_subgraph filter nests
    nicely so you can use the original graph as G in this function
    to avoid chains. We do not rule out chains programmatically so
    that odd cases like an `edge_subgraph` of a `restricted_view`
    can be created.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> H = G.edge_subgraph([(0, 1), (3, 4)])
    >>> list(H.nodes)
    [0, 1, 3, 4]
    >>> list(H.edges)
    [(0, 1), (3, 4)]
    """
    nxf = nx.filters
    edges = set(edges)
    nodes = set()
    for e in edges:
        nodes.update(e[:2])
    induced_nodes = nxf.show_nodes(nodes)
    if G.is_multigraph():
        if G.is_directed():
            induced_edges = nxf.show_multidiedges(edges)
        else:
            induced_edges = nxf.show_multiedges(edges)
    else:
        if G.is_directed():
            induced_edges = nxf.show_diedges(edges)
        else:
            induced_edges = nxf.show_edges(edges)
    return nx.subgraph_view(G, filter_node=induced_nodes, filter_edge=induced_edges)

