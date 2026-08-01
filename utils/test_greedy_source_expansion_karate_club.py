
def test_greedy_source_expansion_karate_club():
    G = nx.karate_club_graph()

    community = nx.community.greedy_source_expansion(G, source=16)

    expected = {0, 4, 5, 6, 10, 16}

    assert community == expected

