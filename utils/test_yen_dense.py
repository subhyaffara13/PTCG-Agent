
def test_yen_dense():
    dense_undirected_G = np.array([
                       [0, 3, 3, 1, 2],
                       [3, 0, 7, 6, 5],
                       [3, 7, 0, 4, 0],
                       [1, 6, 4, 0, 2],
                       [2, 5, 0, 2, 0]], dtype=float)
    distances = yen(
                dense_undirected_G,
                source=0,
                sink=4,
                K=5,
                directed=False,
            )
    assert_allclose(distances, [2., 3., 8., 9., 11.])

