
def test_unconnected_graphs_betweenness_centrality(centrality_func):
    G = nx.Graph([(1, 2), (3, 4)])
    G.add_node(5)
    with pytest.raises(nx.NetworkXError, match="Graph not connected"):
        centrality_func(G)

