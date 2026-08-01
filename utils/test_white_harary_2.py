
def test_white_harary_2():
    # Figure 8 white and harary (2001)
    # https://doi.org/10.1111/0081-1750.00098
    G = nx.disjoint_union(nx.complete_graph(4), nx.complete_graph(4))
    G.add_edge(0, 4)
    # kappa <= lambda <= delta
    assert 3 == min(nx.core_number(G).values())
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        assert 1 == nx.node_connectivity(G, flow_func=flow_func), errmsg
        assert 1 == nx.edge_connectivity(G, flow_func=flow_func), errmsg

