
def test_all_simple_edge_paths_cutoff():
    G = nx.complete_graph(4)
    paths = nx.all_simple_edge_paths(G, 0, 1, cutoff=1)
    assert {tuple(p) for p in paths} == {((0, 1),)}
    paths = nx.all_simple_edge_paths(G, 0, 1, cutoff=2)
    assert {tuple(p) for p in paths} == {((0, 1),), ((0, 2), (2, 1)), ((0, 3), (3, 1))}

