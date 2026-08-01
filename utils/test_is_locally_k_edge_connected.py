
def test_is_locally_k_edge_connected():
    G = nx.barbell_graph(10, 0)
    assert is_locally_k_edge_connected(G, 5, 15, k=1)
    assert not is_locally_k_edge_connected(G, 5, 15, k=2)

    G = nx.Graph()
    G.add_nodes_from([5, 15])
    assert not is_locally_k_edge_connected(G, 5, 15, k=2)

