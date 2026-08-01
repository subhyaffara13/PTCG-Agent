
def test_octahedral_cutset():
    G = nx.octahedral_graph()
    for flow_func in flow_funcs:
        kwargs = {"flow_func": flow_func}
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        # edge cuts
        edge_cut = nx.minimum_edge_cut(G, **kwargs)
        assert 4 == len(edge_cut), errmsg
        H = G.copy()
        H.remove_edges_from(edge_cut)
        assert not nx.is_connected(H), errmsg
        # node cuts
        node_cut = nx.minimum_node_cut(G, **kwargs)
        assert 4 == len(node_cut), errmsg
        H = G.copy()
        H.remove_nodes_from(node_cut)
        assert not nx.is_connected(H), errmsg

