
def test_missing_source():
    G = nx.path_graph(4)
    for flow_func in flow_funcs:
        pytest.raises(
            nx.NetworkXError, nx.node_connectivity, G, 10, 1, flow_func=flow_func
        )


def test_missing_source():
    G = nx.path_graph(4)
    for interface_func in [nx.minimum_edge_cut, nx.minimum_node_cut]:
        for flow_func in flow_funcs:
            pytest.raises(
                nx.NetworkXError, interface_func, G, 10, 1, flow_func=flow_func
            )


def test_missing_source():
    G = nx.path_graph(4)
    pytest.raises(nx.NetworkXError, approx.node_connectivity, G, 10, 1)

