
def test_kdtree_pickle(kdtree_type):
    # test if it is possible to pickle a KDTree
    import pickle
    np.random.seed(0)
    n = 50
    k = 4
    points = np.random.randn(n, k)
    T1 = kdtree_type(points)
    tmp = pickle.dumps(T1)
    T2 = pickle.loads(tmp)
    T1 = T1.query(points, k=5)[-1]
    T2 = T2.query(points, k=5)[-1]
    assert_array_equal(T1, T2)

