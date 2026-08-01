
def remove_edge_attributes(G, *attr_names, ebunch=None):
    """Remove edge attributes from all edges in the graph.

    Parameters
    ----------
    G : NetworkX Graph

    *attr_names : List of Strings
        The attribute names to remove from the graph.

    Examples
    --------
    >>> G = nx.path_graph(3)
    >>> nx.set_edge_attributes(G, {(u, v): u + v for u, v in G.edges()}, name="weight")
    >>> nx.get_edge_attributes(G, "weight")
    {(0, 1): 1, (1, 2): 3}
    >>> remove_edge_attributes(G, "weight")
    >>> nx.get_edge_attributes(G, "weight")
    {}
    """
    if ebunch is None:
        ebunch = G.edges(keys=True) if G.is_multigraph() else G.edges()

    for attr in attr_names:
        edges = (
            G.edges(keys=True, data=True) if G.is_multigraph() else G.edges(data=True)
        )
        for *e, d in edges:
            if tuple(e) in ebunch:
                try:
                    del d[attr]
                except KeyError:
                    pass

