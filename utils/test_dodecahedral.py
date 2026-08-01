
def test_dodecahedral():
    G = nx.dodecahedral_graph()
    for flow_func in flow_funcs:
        errmsg = f"Assertion failed in function: {flow_func.__name__}"
        assert 3 == nx.node_connectivity(G, flow_func=flow_func), errmsg
        assert 3 == nx.edge_connectivity(G, flow_func=flow_func), errmsg


def test_dodecahedral():
    # Actual coefficient is 0
    G = nx.dodecahedral_graph()
    assert average_clustering(G, trials=len(G) // 2) == nx.average_clustering(G)


def test_dodecahedral():
    G = nx.dodecahedral_graph()
    assert 3 == approx.node_connectivity(G)
    assert 3 == approx.node_connectivity(G, 0, 5)

