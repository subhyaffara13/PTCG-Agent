
def test_all_simple_edge_paths_empty_path():
    G = nx.empty_graph(1)
    assert list(nx.all_simple_edge_paths(G, 0, 0)) == [[]]

