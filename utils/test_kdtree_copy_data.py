
def test_kdtree_copy_data(kdtree_type):
    # check if copy_data=True makes the kd-tree
    # impervious to data corruption by modification of
    # the data arrray
    np.random.seed(0)
    n = 5000
    k = 4
    points = np.random.randn(n, k)
    T = kdtree_type(points, copy_data=True)
    q = points.copy()
    T1 = T.query(q, k=5)[-1]
    points[...] = np.random.randn(n, k)
    T2 = T.query(q, k=5)[-1]
    assert_array_equal(T1, T2)

