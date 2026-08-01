
def test_all_triangles_subset_empty():
    G = nx.Graph()
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 0),  # triangle: 0-1-2
            (2, 3),
            (3, 4),
            (4, 2),  # triangle: 2-3-4
            (5, 2),
        ]
    )
    assert list(nx.all_triangles(G, nbunch=[5])) == []

