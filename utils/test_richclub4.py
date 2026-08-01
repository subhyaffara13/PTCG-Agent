
def test_richclub4():
    G = nx.Graph()
    G.add_edges_from(
        [(0, 1), (0, 2), (0, 3), (0, 4), (4, 5), (5, 9), (6, 9), (7, 9), (8, 9)]
    )
    rc = nx.rich_club_coefficient(G, normalized=False)
    assert rc == {0: 18 / 90.0, 1: 6 / 12.0, 2: 0.0, 3: 0.0}

