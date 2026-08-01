
def test_is_aperiodic_null_graph_raises():
    G = nx.DiGraph()
    pytest.raises(nx.NetworkXPointlessConcept, nx.is_aperiodic, G)

