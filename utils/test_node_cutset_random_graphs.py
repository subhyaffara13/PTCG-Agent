
def test_node_cutset_random_graphs():
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        for i in range(3):
            G = nx.fast_gnp_random_graph(50, 0.25, seed=42)
            if not nx.is_connected(G):
                ccs = iter(nx.connected_components(G))
                start = arbitrary_element(next(ccs))
                G.add_edges_from((start, arbitrary_element(c)) for c in ccs)
            cutset = nx.minimum_node_cut(G, flow_func=flow_func)
            assert nx.node_connectivity(G) == len(cutset), errmsg
            G.remove_nodes_from(cutset)
            assert not nx.is_connected(G), errmsg

