
def test_raise_disconnected_graph_connected_dominating_set():
    with pytest.raises(nx.NetworkXError):
        G = nx.Graph()
        G.add_node(1)
        G.add_node(2)
        nx.connected_dominating_set(G)

