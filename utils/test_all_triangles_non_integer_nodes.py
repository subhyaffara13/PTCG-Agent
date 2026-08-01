
def test_all_triangles_non_integer_nodes():
    G = nx.Graph()
    G.add_edges_from(
        [
            ("a", "b"),
            ("b", "c"),
            ("c", "a"),  # triangle: a-b-c
        ]
    )
    expected = {frozenset({"a", "b", "c"})}
    assert {frozenset(t) for t in nx.all_triangles(G)} == expected

