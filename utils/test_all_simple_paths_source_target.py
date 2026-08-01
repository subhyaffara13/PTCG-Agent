
def test_all_simple_paths_source_target():
    G = nx.path_graph(4)
    assert list(nx.all_simple_paths(G, 1, 1)) == [[1]]

