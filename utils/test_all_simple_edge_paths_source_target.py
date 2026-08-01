
def test_all_simple_edge_paths_source_target():
    G = nx.path_graph(4)
    paths = nx.all_simple_edge_paths(G, 1, 1)
    assert list(paths) == [[]]

