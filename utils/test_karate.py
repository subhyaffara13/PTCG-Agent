
def test_karate():
    G = nx.karate_club_graph()
    for flow_func in flow_funcs:
        kwargs = {"flow_func": flow_func}
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        # edge disjoint paths
        edge_dpaths = list(nx.edge_disjoint_paths(G, 0, 33, **kwargs))
        assert are_edge_disjoint_paths(G, edge_dpaths), errmsg
        assert nx.edge_connectivity(G, 0, 33) == len(edge_dpaths), errmsg
        # node disjoint paths
        node_dpaths = list(nx.node_disjoint_paths(G, 0, 33, **kwargs))
        assert are_node_disjoint_paths(G, node_dpaths), errmsg
        assert nx.node_connectivity(G, 0, 33) == len(node_dpaths), errmsg


def test_karate():
    G = nx.karate_club_graph()
    _check_augmentations(G)


def test_karate():
    G = nx.karate_club_graph()
    _check_edge_connectivity(G)


def test_karate():
    G = nx.karate_club_graph()
    result = nx.k_components(G)
    _check_connectivity(G, result)


def test_karate():
    G = nx.karate_club_graph()
    _check_separating_sets(G)

