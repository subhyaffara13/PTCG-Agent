
def test_all_simple_edge_paths():
    G = nx.path_graph(4)
    paths = nx.all_simple_edge_paths(G, 0, 3)
    assert {tuple(p) for p in paths} == {((0, 1), (1, 2), (2, 3))}

