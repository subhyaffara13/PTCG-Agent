
def test_greedy_source_expansion_cutoff():
    G = nx.karate_club_graph()

    community = nx.community.greedy_source_expansion(G, source=16, cutoff=3)

    assert community == {5, 6, 16}

