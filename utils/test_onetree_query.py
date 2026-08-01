
def test_onetree_query(kdtree_type):
    np.random.seed(0)
    n = 50
    k = 4
    points = np.random.randn(n, k)
    T = kdtree_type(points)
    check_onetree_query(T, 0.1)

    points = np.random.randn(3*n, k)
    points[:n] *= 0.001
    points[n:2*n] += 2
    T = kdtree_type(points)
    check_onetree_query(T, 0.1)
    check_onetree_query(T, 0.001)
    check_onetree_query(T, 0.00001)
    check_onetree_query(T, 1e-6)

