
def test_complete_graph_connected_dominating_set():
    K5 = nx.complete_graph(5)
    assert 1 == len(nx.connected_dominating_set(K5))
    K7 = nx.complete_graph(7)
    assert 1 == len(nx.connected_dominating_set(K7))

