
def test_modifies_input(metric):
    # test whether cdist or pdist modifies input arrays
    X1 = np.asarray([[1., 2., 3.],
                     [1.2, 2.3, 3.4],
                     [2.2, 2.3, 4.4],
                     [22.2, 23.3, 44.4]])
    X1_copy = X1.copy()
    cdist(X1, X1, metric)
    pdist(X1, metric)
    assert_array_equal(X1, X1_copy)

