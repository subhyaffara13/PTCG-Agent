
def test_complete_graph():
    G = nx.complete_graph(5)
    assert nx.node_connectivity(G) == 4
    assert list(nx.all_node_cuts(G)) == []

