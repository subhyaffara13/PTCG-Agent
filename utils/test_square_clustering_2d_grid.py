
def test_square_clustering_2d_grid():
    G = nx.grid_2d_graph(3, 3)
    # Central node: 4 squares out of 20 potential
    expected = {
        (0, 0): 1 / 3,
        (0, 1): 0.25,
        (0, 2): 1 / 3,
        (1, 0): 0.25,
        (1, 1): 0.2,
        (1, 2): 0.25,
        (2, 0): 1 / 3,
        (2, 1): 0.25,
        (2, 2): 1 / 3,
    }
    assert nx.square_clustering(G) == expected

