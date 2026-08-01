
def test_brandes_erlebach_book():
    # Figure 1 chapter 7: Connectivity
    # http://www.informatik.uni-augsburg.de/thi/personen/kammer/Graph_Connectivity.pdf
    G = nx.Graph()
    G.add_edges_from(
        [
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 4),
            (3, 6),
            (4, 6),
            (4, 7),
            (5, 7),
            (6, 8),
            (6, 9),
            (7, 8),
            (7, 10),
            (8, 11),
            (9, 10),
            (9, 11),
            (10, 11),
        ]
    )
    for flow_func in flow_funcs:
        kwargs = {"flow_func": flow_func}
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        # edge cutsets
        assert 3 == len(nx.minimum_edge_cut(G, 1, 11, **kwargs)), errmsg
        edge_cut = nx.minimum_edge_cut(G, **kwargs)
        # Node 5 has only two edges
        assert 2 == len(edge_cut), errmsg
        H = G.copy()
        H.remove_edges_from(edge_cut)
        assert not nx.is_connected(H), errmsg
        # node cuts
        assert {6, 7} == minimum_st_node_cut(G, 1, 11, **kwargs), errmsg
        assert {6, 7} == nx.minimum_node_cut(G, 1, 11, **kwargs), errmsg
        node_cut = nx.minimum_node_cut(G, **kwargs)
        assert 2 == len(node_cut), errmsg
        H = G.copy()
        H.remove_nodes_from(node_cut)
        assert not nx.is_connected(H), errmsg

