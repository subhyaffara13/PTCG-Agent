
def test_difference_raise():
    G = nx.path_graph(4)
    H = nx.path_graph(3)
    pytest.raises(nx.NetworkXError, nx.difference, G, H)
    pytest.raises(nx.NetworkXError, nx.symmetric_difference, G, H)

