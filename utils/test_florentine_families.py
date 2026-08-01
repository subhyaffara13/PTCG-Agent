
def test_florentine_families():
    G = nx.florentine_families_graph()
    for flow_func in flow_funcs:
        kwargs = {"flow_func": flow_func}
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        # edge disjoint paths
        edge_dpaths = list(nx.edge_disjoint_paths(G, "Medici", "Strozzi", **kwargs))
        assert are_edge_disjoint_paths(G, edge_dpaths), errmsg
        assert nx.edge_connectivity(G, "Medici", "Strozzi") == len(edge_dpaths), errmsg
        # node disjoint paths
        node_dpaths = list(nx.node_disjoint_paths(G, "Medici", "Strozzi", **kwargs))
        assert are_node_disjoint_paths(G, node_dpaths), errmsg
        assert nx.node_connectivity(G, "Medici", "Strozzi") == len(node_dpaths), errmsg

