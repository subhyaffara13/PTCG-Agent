
def test_tensor_product_combinations():
    # basic smoke test, more realistic tests would be useful
    P5 = nx.path_graph(5)
    K3 = nx.complete_graph(3)
    G = nx.tensor_product(P5, K3)
    assert nx.number_of_nodes(G) == 5 * 3
    G = nx.tensor_product(P5, nx.MultiGraph(K3))
    assert nx.number_of_nodes(G) == 5 * 3
    G = nx.tensor_product(nx.MultiGraph(P5), K3)
    assert nx.number_of_nodes(G) == 5 * 3
    G = nx.tensor_product(nx.MultiGraph(P5), nx.MultiGraph(K3))
    assert nx.number_of_nodes(G) == 5 * 3

    G = nx.tensor_product(nx.DiGraph(P5), nx.DiGraph(K3))
    assert nx.number_of_nodes(G) == 5 * 3

