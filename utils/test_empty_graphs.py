
def test_empty_graphs():
    for k in range(5, 25, 5):
        G = nx.empty_graph(k)
        for flow_func in flow_funcs:
            errmsg = f"Assertion failed in function: {flow_func.__name__}"
            assert 0 == nx.node_connectivity(G, flow_func=flow_func), errmsg
            assert 0 == nx.edge_connectivity(G, flow_func=flow_func), errmsg


def test_empty_graphs():
    G = nx.Graph()
    D = nx.DiGraph()
    for interface_func in [nx.minimum_node_cut, nx.minimum_edge_cut]:
        for flow_func in flow_funcs:
            pytest.raises(
                nx.NetworkXPointlessConcept, interface_func, G, flow_func=flow_func
            )
            pytest.raises(
                nx.NetworkXPointlessConcept, interface_func, D, flow_func=flow_func
            )


def test_empty_graphs():
    for k in range(5, 25, 5):
        G = nx.empty_graph(k)
        assert 0 == approx.node_connectivity(G)
        assert 0 == approx.node_connectivity(G, 0, 3)

