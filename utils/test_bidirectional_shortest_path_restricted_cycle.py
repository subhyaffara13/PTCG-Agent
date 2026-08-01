
def test_bidirectional_shortest_path_restricted_cycle():
    cycle = nx.cycle_graph(7)
    length, path = _bidirectional_shortest_path(cycle, 0, 3)
    assert path == [0, 1, 2, 3]
    length, path = _bidirectional_shortest_path(cycle, 0, 3, ignore_nodes=[1])
    assert path == [0, 6, 5, 4, 3]

