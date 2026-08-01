
def test_bidirectional_shortest_path_restricted_directed_cycle():
    directed_cycle = nx.cycle_graph(7, create_using=nx.DiGraph())
    length, path = _bidirectional_shortest_path(directed_cycle, 0, 3)
    assert path == [0, 1, 2, 3]
    pytest.raises(
        nx.NetworkXNoPath,
        _bidirectional_shortest_path,
        directed_cycle,
        0,
        3,
        ignore_nodes=[1],
    )
    length, path = _bidirectional_shortest_path(
        directed_cycle, 0, 3, ignore_edges=[(2, 1)]
    )
    assert path == [0, 1, 2, 3]
    pytest.raises(
        nx.NetworkXNoPath,
        _bidirectional_shortest_path,
        directed_cycle,
        0,
        3,
        ignore_edges=[(1, 2)],
    )

