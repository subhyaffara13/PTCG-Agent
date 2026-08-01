
def test_all_simple_paths_source_in_targets():
    # See GitHub issue #6690.
    G = nx.path_graph(3)
    assert list(nx.all_simple_paths(G, 0, {0, 1, 2})) == [[0], [0, 1], [0, 1, 2]]

