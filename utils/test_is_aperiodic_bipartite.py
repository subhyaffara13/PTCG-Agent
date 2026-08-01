
def test_is_aperiodic_bipartite():
    # Bipartite graph
    G = nx.DiGraph(nx.davis_southern_women_graph())
    assert not nx.is_aperiodic(G)

