
def test_all_triangles_no_triangles():
    G = nx.path_graph(4)
    assert list(nx.all_triangles(G)) == []

