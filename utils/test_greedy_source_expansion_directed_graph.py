
def test_greedy_source_expansion_directed_graph():
    G_edges = [
        (0, 2),
        (0, 1),
        (1, 0),
        (2, 1),
        (2, 0),
        (3, 4),
        (4, 3),
        (4, 5),
        (5, 3),
        (5, 6),
        (0, 6),
    ]
    G = nx.DiGraph(G_edges)

    expected = {0, 1, 2, 6}
    community = nx.community.greedy_source_expansion(G, source=0)
    assert community == expected

