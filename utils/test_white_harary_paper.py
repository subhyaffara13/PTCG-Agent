
def test_white_harary_paper():
    # Figure 1b white and harary (2001)
    # https://doi.org/10.1111/0081-1750.00098
    # A graph with high adhesion (edge connectivity) and low cohesion
    # (node connectivity)
    G = nx.disjoint_union(nx.complete_graph(4), nx.complete_graph(4))
    G.remove_node(7)
    for i in range(4, 7):
        G.add_edge(0, i)
    G = nx.disjoint_union(G, nx.complete_graph(4))
    G.remove_node(G.order() - 1)
    for i in range(7, 10):
        G.add_edge(0, i)
    for flow_func in flow_funcs:
        kwargs = {"flow_func": flow_func}
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        # edge cuts
        edge_cut = nx.minimum_edge_cut(G, **kwargs)
        assert 3 == len(edge_cut), errmsg
        H = G.copy()
        H.remove_edges_from(edge_cut)
        assert not nx.is_connected(H), errmsg
        # node cuts
        node_cut = nx.minimum_node_cut(G, **kwargs)
        assert {0} == node_cut, errmsg
        H = G.copy()
        H.remove_nodes_from(node_cut)
        assert not nx.is_connected(H), errmsg

