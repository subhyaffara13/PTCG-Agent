
def test_connected_double_edge_swap_small():
    with pytest.raises(nx.NetworkXError):
        G = nx.connected_double_edge_swap(nx.path_graph(3))

