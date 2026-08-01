
def test_rich_club_leq_3_nodes_unnormalized():
    # edgeless graphs upto 3 nodes
    G = nx.Graph()
    rc = nx.rich_club_coefficient(G, normalized=False)
    assert rc == {}

    for i in range(3):
        G.add_node(i)
        rc = nx.rich_club_coefficient(G, normalized=False)
        assert rc == {}

    # 2 nodes, single edge
    G = nx.Graph()
    G.add_edge(0, 1)
    rc = nx.rich_club_coefficient(G, normalized=False)
    assert rc == {0: 1}

    # 3 nodes, single edge
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2])
    G.add_edge(0, 1)
    rc = nx.rich_club_coefficient(G, normalized=False)
    assert rc == {0: 1}

    # 3 nodes, 2 edges
    G.add_edge(1, 2)
    rc = nx.rich_club_coefficient(G, normalized=False)
    assert rc == {0: 2 / 3}

    # 3 nodes, 3 edges
    G.add_edge(0, 2)
    rc = nx.rich_club_coefficient(G, normalized=False)
    assert rc == {0: 1, 1: 1}

