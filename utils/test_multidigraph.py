
def test_multidigraph():
    G = nx.MultiDiGraph()
    nx.add_path(G, [1, 2, 3])
    H = cytoscape_graph(cytoscape_data(G))
    assert H.is_directed()
    assert H.is_multigraph()


def test_multidigraph():
    """Multidigraphs are acceptable."""
    G = nx.MultiDiGraph()
    G.add_weighted_edges_from([(1, 2, 1), (2, 3, 2)], weight="capacity")
    flowCost, H = nx.network_simplex(G)
    assert flowCost == 0
    assert H == {1: {2: {0: 0}}, 2: {3: {0: 0}}, 3: {}}

