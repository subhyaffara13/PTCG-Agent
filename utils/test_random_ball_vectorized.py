
def test_random_ball_vectorized(kdtree_type):
    n = 20
    m = 5
    np.random.seed(1234)
    T = kdtree_type(np.random.randn(n, m))

    r = T.query_ball_point(np.random.randn(2, 3, m), 1)
    assert_equal(r.shape, (2, 3))
    assert_(isinstance(r[0, 0], list))

