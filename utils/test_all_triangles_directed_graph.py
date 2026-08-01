
def test_all_triangles_directed_graph():
    G = nx.DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    with pytest.raises(nx.NetworkXNotImplemented):
        list(nx.all_triangles(G))

