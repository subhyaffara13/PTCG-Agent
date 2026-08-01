
def test_complete_graphs():
    for n in range(5, 20, 5):
        for flow_func in flow_funcs:
            G = nx.complete_graph(n)
            errmsg = f"Assertion failed in function: {flow_func.__name__}"
            assert n - 1 == nx.node_connectivity(G, flow_func=flow_func), errmsg
            assert n - 1 == nx.node_connectivity(
                G.to_directed(), flow_func=flow_func
            ), errmsg
            assert n - 1 == nx.edge_connectivity(G, flow_func=flow_func), errmsg
            assert n - 1 == nx.edge_connectivity(
                G.to_directed(), flow_func=flow_func
            ), errmsg


def test_complete_graphs():
    for n in range(5, 25, 5):
        G = nx.complete_graph(n)
        assert n - 1 == approx.node_connectivity(G)
        assert n - 1 == approx.node_connectivity(G, 0, 3)

