
def test_less_than_3_edges():
    G = nx.DiGraph([(0, 1), (1, 2)])
    G.add_nodes_from([3, 4])
    with pytest.raises(nx.NetworkXError, match=".*fewer than 3 edges"):
        nx.directed_edge_swap(G)

    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3])
    with pytest.raises(nx.NetworkXError, match=".*fewer than 2 edges"):
        nx.double_edge_swap(G)

