
def test_is_aperiodic_disconnected_raises():
    G = nx.DiGraph()
    nx.add_cycle(G, [0, 1, 2])
    G.add_edge(3, 3)
    pytest.raises(nx.NetworkXError, nx.is_aperiodic, G)

