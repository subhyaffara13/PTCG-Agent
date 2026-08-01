
def test_null_graph_connected_dominating_set():
    G = nx.Graph()
    assert 0 == len(nx.connected_dominating_set(G))

