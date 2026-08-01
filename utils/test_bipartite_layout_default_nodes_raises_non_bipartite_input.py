
def test_bipartite_layout_default_nodes_raises_non_bipartite_input():
    G = nx.complete_graph(5)
    with pytest.raises(nx.NetworkXError, match="Graph is not bipartite"):
        nx.bipartite_layout(G)
    # No exception if nodes are explicitly specified
    pos = nx.bipartite_layout(G, nodes=[2, 3])

