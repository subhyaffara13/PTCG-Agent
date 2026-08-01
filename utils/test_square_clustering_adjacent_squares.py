
def test_square_clustering_adjacent_squares():
    G = nx.Graph([(1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6)])
    # Corner nodes: C_4 == 0.5, central face nodes: C_4 = 1 / 3
    expected = {1: 0.5, 2: 0.5, 3: 1 / 3, 4: 1 / 3, 5: 0.5, 6: 0.5}
    assert nx.square_clustering(G) == expected

