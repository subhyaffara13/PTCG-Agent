
def test_zero_weight():
    G = nx.DiGraph()
    edges = [(1, 2, -2), (2, 3, -4), (1, 5, 1), (5, 4, 0), (4, 3, -5), (2, 5, -7)]
    G.add_weighted_edges_from(edges)
    dist = nx.floyd_warshall_numpy(G)
    assert int(np.min(dist)) == -14

    G = nx.MultiDiGraph()
    edges.append((2, 5, -7))
    G.add_weighted_edges_from(edges)
    dist = nx.floyd_warshall_numpy(G)
    assert int(np.min(dist)) == -14

