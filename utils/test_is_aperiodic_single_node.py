
def test_is_aperiodic_single_node():
    G = nx.DiGraph()
    G.add_node(0)
    assert not nx.is_aperiodic(G)
    G.add_edge(0, 0)
    assert nx.is_aperiodic(G)

