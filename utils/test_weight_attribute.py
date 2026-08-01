
def test_weight_attribute():
    G = nx.Graph()
    G.add_weighted_edges_from([(0, 1, 1.0), (1, 2, 3.5)], weight="w")
    expected = {0: 3.431, 1: 3.082, 2: 5.612}
    b = nx.second_order_centrality(G, weight="w")

    for n in sorted(G):
        assert b[n] == pytest.approx(expected[n], abs=1e-2)

