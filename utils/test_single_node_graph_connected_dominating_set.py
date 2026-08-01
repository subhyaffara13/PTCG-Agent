
def test_single_node_graph_connected_dominating_set():
    G = nx.Graph()
    G.add_node(1)
    CD = nx.connected_dominating_set(G)
    assert nx.is_connected_dominating_set(G, CD)

