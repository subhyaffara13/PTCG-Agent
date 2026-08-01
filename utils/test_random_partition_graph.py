
def test_random_partition_graph():
    G = nx.random_partition_graph([3, 3, 3], 1, 0, seed=42)
    C = G.graph["partition"]
    assert C == [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}]
    assert len(G) == 9
    assert len(list(G.edges())) == 9

    G = nx.random_partition_graph([3, 3, 3], 0, 1)
    C = G.graph["partition"]
    assert C == [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}]
    assert len(G) == 9
    assert len(list(G.edges())) == 27

    G = nx.random_partition_graph([3, 3, 3], 1, 0, directed=True)
    C = G.graph["partition"]
    assert C == [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}]
    assert len(G) == 9
    assert len(list(G.edges())) == 18

    G = nx.random_partition_graph([3, 3, 3], 0, 1, directed=True)
    C = G.graph["partition"]
    assert C == [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}]
    assert len(G) == 9
    assert len(list(G.edges())) == 54

    G = nx.random_partition_graph([1, 2, 3, 4, 5], 0.5, 0.1)
    C = G.graph["partition"]
    assert C == [{0}, {1, 2}, {3, 4, 5}, {6, 7, 8, 9}, {10, 11, 12, 13, 14}]
    assert len(G) == 15

    rpg = nx.random_partition_graph
    pytest.raises(nx.NetworkXError, rpg, [1, 2, 3], 1.1, 0.1)
    pytest.raises(nx.NetworkXError, rpg, [1, 2, 3], -0.1, 0.1)
    pytest.raises(nx.NetworkXError, rpg, [1, 2, 3], 0.1, 1.1)
    pytest.raises(nx.NetworkXError, rpg, [1, 2, 3], 0.1, -0.1)

