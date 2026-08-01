
def test_empty_is_biconnected():
    G = nx.empty_graph(5)
    assert not nx.is_biconnected(G)
    G.add_edge(0, 1)
    assert not nx.is_biconnected(G)

