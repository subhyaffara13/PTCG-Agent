
def test_edge_missing_target():
    G = nx.path_graph(4)
    for flow_func in flow_funcs:
        pytest.raises(
            nx.NetworkXError, nx.edge_connectivity, G, 1, 10, flow_func=flow_func
        )

