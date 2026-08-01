
def test_all_triangles_subset():
    G = nx.Graph()
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 0),  # triangle: 0-1-2
            (2, 3),
            (3, 4),
            (4, 2),  # triangle: 2-3-4
        ]
    )
    assert {frozenset(t) for t in nx.all_triangles(G, nbunch=[0, 1])} == {
        frozenset({0, 1, 2})
    }

