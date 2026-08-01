
def test_all_simple_edge_paths_multigraph_with_cutoff():
    G = nx.MultiGraph([(1, 2), (1, 2), (1, 10), (10, 2)])
    paths = list(nx.all_simple_edge_paths(G, 1, 2, cutoff=1))
    assert len(paths) == 2
    assert {tuple(p) for p in paths} == {((1, 2, 0),), ((1, 2, 1),)}

