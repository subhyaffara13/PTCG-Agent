
def test_shortest_simple_paths_singleton_path():
    G = nx.empty_graph(3)
    assert list(nx.shortest_simple_paths(G, 0, 0)) == [[0]]

