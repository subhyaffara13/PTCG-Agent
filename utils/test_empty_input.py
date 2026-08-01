
def test_empty_input():
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        czt([])
    with pytest.raises(ValueError, match='Invalid number of CZT'):
        zoom_fft([], 0.5)


def test_empty_input():
    G = nx.Graph()
    assert [] == list(nx.k_edge_components(G, k=5))
    assert [] == list(nx.k_edge_subgraphs(G, k=5))

    G = nx.DiGraph()
    assert [] == list(nx.k_edge_components(G, k=5))
    assert [] == list(nx.k_edge_subgraphs(G, k=5))

