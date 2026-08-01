
def test_is_aperiodic_weakly_connected_raises():
    G = nx.DiGraph([(1, 2), (2, 3)])
    pytest.raises(nx.NetworkXError, nx.is_aperiodic, G)

