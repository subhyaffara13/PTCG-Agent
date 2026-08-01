
def test_digraph():
    G = nx.DiGraph()
    nx.add_path(G, [1, 2, 3])
    H = cytoscape_graph(cytoscape_data(G))
    assert H.is_directed()
    assert nx.is_isomorphic(G, H)

