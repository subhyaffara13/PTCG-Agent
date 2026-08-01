
def test_is_biconnected():
    G = nx.cycle_graph(3)
    assert nx.is_biconnected(G)
    nx.add_cycle(G, [1, 3, 4])
    assert not nx.is_biconnected(G)

