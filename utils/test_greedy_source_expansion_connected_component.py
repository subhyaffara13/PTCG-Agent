
def test_greedy_source_expansion_connected_component():
    G_edges = [(0, 2), (0, 1), (1, 0), (2, 1), (2, 0), (3, 4), (4, 3)]
    G = nx.Graph(G_edges)
    expected = {0, 1, 2}
    community = nx.community.greedy_source_expansion(G, source=0)
    assert community == expected

