
def test_biconnected_components1():
    # graph example from
    # https://web.archive.org/web/20121229123447/http://www.ibluemojo.com/school/articul_algorithm.html
    edges = [
        (0, 1),
        (0, 5),
        (0, 6),
        (0, 14),
        (1, 5),
        (1, 6),
        (1, 14),
        (2, 4),
        (2, 10),
        (3, 4),
        (3, 15),
        (4, 6),
        (4, 7),
        (4, 10),
        (5, 14),
        (6, 14),
        (7, 9),
        (8, 9),
        (8, 12),
        (8, 13),
        (10, 15),
        (11, 12),
        (11, 13),
        (12, 13),
    ]
    G = nx.Graph(edges)
    pts = set(nx.articulation_points(G))
    assert pts == {4, 6, 7, 8, 9}
    comps = list(nx.biconnected_component_edges(G))
    answer = [
        [(3, 4), (15, 3), (10, 15), (10, 4), (2, 10), (4, 2)],
        [(13, 12), (13, 8), (11, 13), (12, 11), (8, 12)],
        [(9, 8)],
        [(7, 9)],
        [(4, 7)],
        [(6, 4)],
        [(14, 0), (5, 1), (5, 0), (14, 5), (14, 1), (6, 14), (6, 0), (1, 6), (0, 1)],
    ]
    assert_components_edges_equal(comps, answer)

