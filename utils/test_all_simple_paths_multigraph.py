
def test_all_simple_paths_multigraph():
    G = nx.MultiGraph([(1, 2), (1, 2)])
    assert list(nx.all_simple_paths(G, 1, 1)) == [[1]]
    nx.add_path(G, [3, 1, 10, 2])
    paths = list(nx.all_simple_paths(G, 1, 2))
    assert len(paths) == 3
    assert {tuple(p) for p in paths} == {(1, 2), (1, 2), (1, 10, 2)}

