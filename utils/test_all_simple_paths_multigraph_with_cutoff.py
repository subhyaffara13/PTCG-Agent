
def test_all_simple_paths_multigraph_with_cutoff():
    G = nx.MultiGraph([(1, 2), (1, 2), (1, 10), (10, 2)])
    paths = list(nx.all_simple_paths(G, 1, 2, cutoff=1))
    assert len(paths) == 2
    assert {tuple(p) for p in paths} == {(1, 2), (1, 2)}

    # See GitHub issue #6732.
    G = nx.MultiGraph([(0, 1), (0, 2)])
    assert list(nx.all_simple_paths(G, 0, {1, 2}, cutoff=1)) == [[0, 1], [0, 2]]

