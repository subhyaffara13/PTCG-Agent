
def test_weak_connections2():
    X = np.array([[0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0],
                  [0, 0, 1, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0]])
    n_components, labels =\
        csgraph.connected_components(X, directed=True,
                                     connection='weak')
    assert_equal(n_components, 2)
    labels.sort()
    assert_array_almost_equal(labels, [0, 0, 1, 1, 1, 1])

