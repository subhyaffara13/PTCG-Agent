
def test_not_connected():
    G = nx.Graph()
    nx.add_path(G, [1, 2, 3])
    nx.add_path(G, [4, 5])
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        assert nx.node_connectivity(G) == 0, errmsg
        assert nx.edge_connectivity(G) == 0, errmsg


def test_not_connected():
    G = nx.Graph()
    nx.add_path(G, [1, 2, 3])
    nx.add_path(G, [4, 5])
    for interface_func in [nx.minimum_edge_cut, nx.minimum_node_cut]:
        for flow_func in flow_funcs:
            pytest.raises(nx.NetworkXError, interface_func, G, flow_func=flow_func)

