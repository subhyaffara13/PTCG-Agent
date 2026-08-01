
def test_square_clustering_multiple_squares_non_complete():
    """An example where all nodes are part of all squares, but not every node
    is connected to every other."""
    G = nx.Graph([(0, 1), (0, 2), (1, 3), (2, 3), (1, 4), (2, 4), (1, 5), (2, 5)])
    expected = {n: 1 for n in G}
    assert nx.square_clustering(G) == expected

