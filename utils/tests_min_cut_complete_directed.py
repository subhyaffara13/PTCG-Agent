
def tests_min_cut_complete_directed():
    G = nx.complete_graph(5)
    G = G.to_directed()
    for interface_func in [nx.minimum_edge_cut, nx.minimum_node_cut]:
        for flow_func in flow_funcs:
            assert 4 == len(interface_func(G, flow_func=flow_func))

