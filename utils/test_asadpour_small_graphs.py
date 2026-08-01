
def test_asadpour_small_graphs():
    # 1 node
    G = nx.path_graph(1, create_using=nx.DiGraph)
    with pytest.raises(nx.NetworkXError, match="at least two nodes"):
        nx_app.asadpour_atsp(G)

    # 2 nodes
    G = nx.DiGraph()
    G.add_weighted_edges_from([(0, 1, 7), (1, 0, 8)])
    assert nx_app.asadpour_atsp(G) in [[0, 1], [1, 0]]
    assert nx_app.asadpour_atsp(G, source=1) == [1, 0]
    assert nx_app.asadpour_atsp(G, source=0) == [0, 1]

