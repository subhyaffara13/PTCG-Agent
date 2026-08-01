
def test_greedy_source_expansion_invalid_method():
    G = nx.karate_club_graph()

    with pytest.raises(ValueError):
        nx.community.greedy_source_expansion(G, source=16, cutoff=3, method="invalid")

