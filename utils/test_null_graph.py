
def test_null_graph():
    G = nx.Graph()
    _check_augmentations(G, max_k=MAX_EFFICIENT_K + 2)


def test_null_graph():
    G = nx.Graph()
    assert not nx.is_biconnected(G)
    assert list(nx.biconnected_components(G)) == []
    assert list(nx.biconnected_component_edges(G)) == []
    assert list(nx.articulation_points(G)) == []

