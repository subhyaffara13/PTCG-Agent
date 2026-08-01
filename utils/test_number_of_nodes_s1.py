
def test_number_of_nodes_S1():
    G = nx.geometric_soft_configuration_graph(
        beta=1.5, n=100, gamma=2.7, mean_degree=10, seed=42
    )
    assert len(G) == 100

