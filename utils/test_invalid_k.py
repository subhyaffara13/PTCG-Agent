
def test_invalid_k():
    G = nx.Graph()
    pytest.raises(ValueError, list, k_edge_augmentation(G, k=-1))
    pytest.raises(ValueError, list, k_edge_augmentation(G, k=0))

