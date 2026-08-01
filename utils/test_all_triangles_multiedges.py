
def test_all_triangles_multiedges(graph_type):
    G = graph_type()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 2)])
    assert {frozenset(t) for t in nx.all_triangles(G)} == {frozenset({0, 1, 2})}

