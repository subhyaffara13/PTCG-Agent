
def test_all_simple_paths_directed():
    G = nx.DiGraph()
    nx.add_path(G, [1, 2, 3])
    nx.add_path(G, [3, 2, 1])
    paths = nx.all_simple_paths(G, 1, 3)
    assert {tuple(p) for p in paths} == {(1, 2, 3)}

