
def test_general_k_edge_subgraph_quick_return():
    # tests quick return optimization
    G = nx.Graph()
    G.add_node(0)
    subgraphs = list(general_k_edge_subgraphs(G, k=1))
    assert len(subgraphs) == 1
    for subgraph in subgraphs:
        assert subgraph.number_of_nodes() == 1

    G.add_node(1)
    subgraphs = list(general_k_edge_subgraphs(G, k=1))
    assert len(subgraphs) == 2
    for subgraph in subgraphs:
        assert subgraph.number_of_nodes() == 1

