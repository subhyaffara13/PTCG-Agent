
def test_edge_missing_source():
    G = nx.path_graph(4)
    for flow_func in flow_funcs:
        pytest.raises(
            nx.NetworkXError, nx.edge_connectivity, G, 10, 1, flow_func=flow_func
        )

