
def test_all_simple_edge_paths_with_two_targets_cutoff():
    G = nx.path_graph(4)
    G.add_edge(2, 4)
    paths = nx.all_simple_edge_paths(G, 0, [3, 4], cutoff=3)
    assert {tuple(p) for p in paths} == {
        ((0, 1), (1, 2), (2, 3)),
        ((0, 1), (1, 2), (2, 4)),
    }

