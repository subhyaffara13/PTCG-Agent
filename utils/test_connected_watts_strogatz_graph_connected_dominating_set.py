
def test_connected_watts_strogatz_graph_connected_dominating_set(n, k, p, seed):
    G = nx.connected_watts_strogatz_graph(n, k, p, seed=seed)
    D = nx.connected_dominating_set(G)
    assert nx.is_connected_dominating_set(G, D)

