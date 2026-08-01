
def test_is_aperiodic_undirected_raises():
    G = nx.Graph([(1, 2), (2, 3), (3, 1)])
    pytest.raises(nx.NetworkXError, nx.is_aperiodic, G)

