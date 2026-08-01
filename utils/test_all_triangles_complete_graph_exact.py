
def test_all_triangles_complete_graph_exact():
    G = nx.complete_graph(4)

    expected = {
        frozenset({0, 1, 2}),
        frozenset({0, 1, 3}),
        frozenset({0, 2, 3}),
        frozenset({1, 2, 3}),
    }

    assert {frozenset(t) for t in nx.all_triangles(G)} == expected

