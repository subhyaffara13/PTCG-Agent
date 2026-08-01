
def test_no_redundant_nodes():
    G = complete_bipartite_graph(2, 2)

    # when nodes is None
    rc = node_redundancy(G)
    assert all(redundancy == 1 for redundancy in rc.values())

    # when set of nodes is specified
    rc = node_redundancy(G, (2, 3))
    assert rc == {2: 1.0, 3: 1.0}

