
def test_average_connectivity_directed():
    G = nx.DiGraph([(1, 3), (1, 4), (1, 5)])
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        assert nx.average_node_connectivity(G) == 0.25, errmsg

