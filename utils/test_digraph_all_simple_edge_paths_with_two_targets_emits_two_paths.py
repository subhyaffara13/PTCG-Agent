
def test_digraph_all_simple_edge_paths_with_two_targets_emits_two_paths():
    G = nx.path_graph(4, create_using=nx.DiGraph())
    G.add_edge(2, 4)
    paths = nx.all_simple_edge_paths(G, 0, [3, 4])
    assert {tuple(p) for p in paths} == {
        ((0, 1), (1, 2), (2, 3)),
        ((0, 1), (1, 2), (2, 4)),
    }

