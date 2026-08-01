
def test_missing_target():
    G = nx.path_graph(4)
    for flow_func in flow_funcs:
        pytest.raises(
            nx.NetworkXError, nx.node_connectivity, G, 1, 10, flow_func=flow_func
        )


def test_missing_target():
    G = nx.path_graph(4)
    for interface_func in [nx.minimum_edge_cut, nx.minimum_node_cut]:
        for flow_func in flow_funcs:
            pytest.raises(
                nx.NetworkXError, interface_func, G, 1, 10, flow_func=flow_func
            )


def test_missing_target():
    G = nx.path_graph(4)
    pytest.raises(nx.NetworkXError, approx.node_connectivity, G, 1, 10)

