
def test_zero_k_exception():
    G = nx.Graph()
    # functions that return generators error immediately
    pytest.raises(ValueError, nx.k_edge_components, G, k=0)
    pytest.raises(ValueError, nx.k_edge_subgraphs, G, k=0)

    # actual generators only error when you get the first item
    aux_graph = EdgeComponentAuxGraph.construct(G)
    pytest.raises(ValueError, list, aux_graph.k_edge_components(k=0))
    pytest.raises(ValueError, list, aux_graph.k_edge_subgraphs(k=0))

    pytest.raises(ValueError, list, general_k_edge_subgraphs(G, k=0))

