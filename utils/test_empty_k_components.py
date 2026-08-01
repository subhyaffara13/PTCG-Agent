
def test_empty_k_components():
    G = nx.empty_graph(5)
    assert nx.k_components(G) == {}

