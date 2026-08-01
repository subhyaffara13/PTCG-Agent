
def test_cutoff():
    G = nx.complete_graph(5)
    for local_func in [local_edge_connectivity, local_node_connectivity]:
        for flow_func in flow_funcs:
            if flow_func is flow.preflow_push:
                # cutoff is not supported by preflow_push
                continue
            for cutoff in [3, 2, 1]:
                result = local_func(G, 0, 4, flow_func=flow_func, cutoff=cutoff)
                assert cutoff == result, f"cutoff error in {flow_func.__name__}"

