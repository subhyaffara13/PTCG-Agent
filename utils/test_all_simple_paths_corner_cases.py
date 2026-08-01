
def test_all_simple_paths_corner_cases():
    assert list(nx.all_simple_paths(nx.empty_graph(2), 0, 0)) == [[0]]
    assert list(nx.all_simple_paths(nx.empty_graph(2), 0, 1)) == []
    assert list(nx.all_simple_paths(nx.path_graph(9), 0, 8, 0)) == []

