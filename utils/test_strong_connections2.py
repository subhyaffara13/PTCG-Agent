
def test_strong_connections2():
    X = np.array([[0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0],
                  [0, 0, 1, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0]])
    n_components, labels =\
        csgraph.connected_components(X, directed=True,
                                     connection='strong')
    assert_equal(n_components, 5)
    labels.sort()
    assert_array_almost_equal(labels, [0, 1, 2, 2, 3, 4])

