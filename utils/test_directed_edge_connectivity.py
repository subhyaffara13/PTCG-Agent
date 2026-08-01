
def test_directed_edge_connectivity():
    G = nx.cycle_graph(10, create_using=nx.DiGraph())  # only one direction
    D = nx.cycle_graph(10).to_directed()  # 2 reciprocal edges
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        assert 1 == nx.edge_connectivity(G, flow_func=flow_func), errmsg
        assert 1 == local_edge_connectivity(G, 1, 4, flow_func=flow_func), errmsg
        assert 1 == nx.edge_connectivity(G, 1, 4, flow_func=flow_func), errmsg
        assert 2 == nx.edge_connectivity(D, flow_func=flow_func), errmsg
        assert 2 == local_edge_connectivity(D, 1, 4, flow_func=flow_func), errmsg
        assert 2 == nx.edge_connectivity(D, 1, 4, flow_func=flow_func), errmsg

