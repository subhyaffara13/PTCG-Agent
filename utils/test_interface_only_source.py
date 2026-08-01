
def test_interface_only_source():
    G = nx.complete_graph(5)
    for interface_func in [nx.node_connectivity, nx.edge_connectivity]:
        pytest.raises(nx.NetworkXError, interface_func, G, s=0)


def test_interface_only_source():
    G = nx.complete_graph(5)
    for interface_func in [nx.minimum_node_cut, nx.minimum_edge_cut]:
        pytest.raises(nx.NetworkXError, interface_func, G, s=0)

