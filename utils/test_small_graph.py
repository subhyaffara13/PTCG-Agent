
def test_small_graph():
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(2, 3)
    assert nx.is_kl_connected(G, 2, 2)
    H = nx.kl_connected_subgraph(G, 2, 2)
    (H, graphOK) = nx.kl_connected_subgraph(
        G, 2, 2, low_memory=True, same_as_graph=True
    )
    assert graphOK

