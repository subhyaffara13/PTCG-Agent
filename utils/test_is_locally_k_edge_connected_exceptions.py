
def test_is_locally_k_edge_connected_exceptions():
    pytest.raises(nx.NetworkXNotImplemented, is_k_edge_connected, nx.DiGraph(), k=0)
    pytest.raises(nx.NetworkXNotImplemented, is_k_edge_connected, nx.MultiGraph(), k=0)
    pytest.raises(ValueError, is_k_edge_connected, nx.Graph(), k=0)

