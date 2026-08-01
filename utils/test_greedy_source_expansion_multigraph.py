
def test_greedy_source_expansion_multigraph():
    G = nx.MultiGraph(nx.karate_club_graph())
    G.add_edge(0, 1)
    G.add_edge(0, 9)

    expected = {0, 4, 5, 6, 10, 16}

    community = nx.community.greedy_source_expansion(G, source=16)

    assert community == expected

