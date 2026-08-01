
def test_short_knn(kdtree_type):

    # The test case is based on github: #6425 by @SteveDoyle2

    xyz = np.array([
        [0., 0., 0.],
        [1.01, 0., 0.],
        [0., 1., 0.],
        [0., 1.01, 0.],
        [1., 0., 0.],
        [1., 1., 0.]],
    dtype='float64')

    ckdt = kdtree_type(xyz)

    deq, ieq = ckdt.query(xyz, k=4, distance_upper_bound=0.2)

    assert_array_almost_equal(deq,
            [[0., np.inf, np.inf, np.inf],
            [0., 0.01, np.inf, np.inf],
            [0., 0.01, np.inf, np.inf],
            [0., 0.01, np.inf, np.inf],
            [0., 0.01, np.inf, np.inf],
            [0., np.inf, np.inf, np.inf]])

