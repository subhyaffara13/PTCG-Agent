
def test_tensor_product_size():
    P5 = nx.path_graph(5)
    K3 = nx.complete_graph(3)
    K5 = nx.complete_graph(5)

    G = nx.tensor_product(P5, K3)
    assert nx.number_of_nodes(G) == 5 * 3
    G = nx.tensor_product(K3, K5)
    assert nx.number_of_nodes(G) == 3 * 5

