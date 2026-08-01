
def test_connected_caveman_graph():
    G = nx.connected_caveman_graph(4, 3)
    assert len(G) == 12

    G = nx.connected_caveman_graph(1, 5)
    K5 = nx.complete_graph(5)
    K5.remove_edge(3, 4)
    assert nx.is_isomorphic(G, K5)

    # need at least 2 nodes in each clique
    pytest.raises(nx.NetworkXError, nx.connected_caveman_graph, 4, 1)

