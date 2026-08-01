
def test_all_simple_edge_paths_ignores_self_loop():
    G = nx.Graph([(0, 0), (0, 1), (1, 1), (1, 2)])
    assert list(nx.all_simple_edge_paths(G, 0, 2)) == [[(0, 1), (1, 2)]]

