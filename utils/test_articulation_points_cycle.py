
def test_articulation_points_cycle():
    G = nx.cycle_graph(3)
    nx.add_cycle(G, [1, 3, 4])
    pts = set(nx.articulation_points(G))
    assert pts == {1}

