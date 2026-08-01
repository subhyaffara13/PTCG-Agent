
def test_all_triangles_overlapping():
    G = nx.Graph()
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 0),  # triangle: 0-1-2
            (0, 2),
            (2, 3),
            (3, 0),  # triangle: 0-2-3
        ]
    )
    expected = {frozenset({0, 1, 2}), frozenset({0, 2, 3})}
    assert {frozenset(t) for t in nx.all_triangles(G)} == expected

