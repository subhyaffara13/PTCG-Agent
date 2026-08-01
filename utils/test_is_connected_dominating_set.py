
def test_is_connected_dominating_set():
    G = nx.path_graph(4)
    D = {1, 2}
    assert nx.is_connected_dominating_set(G, D)
    D = {1, 3}
    assert not nx.is_connected_dominating_set(G, D)
    D = {2, 3}
    assert nx.is_connected(nx.subgraph(G, D))
    assert not nx.is_connected_dominating_set(G, D)

