
def test_all_simple_edge_paths_ignores_cycle():
    G = nx.cycle_graph(3, create_using=nx.DiGraph())
    G.add_edge(1, 3)
    paths = nx.all_simple_edge_paths(G, 0, 3)
    assert {tuple(p) for p in paths} == {((0, 1), (1, 3))}

