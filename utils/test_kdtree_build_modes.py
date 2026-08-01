
def test_kdtree_build_modes(kdtree_type):
    # check if different build modes for KDTree give similar query results
    np.random.seed(0)
    n = 5000
    k = 4
    points = np.random.randn(n, k)
    T1 = kdtree_type(points).query(points, k=5)[-1]
    T2 = kdtree_type(points, compact_nodes=False).query(points, k=5)[-1]
    T3 = kdtree_type(points, balanced_tree=False).query(points, k=5)[-1]
    T4 = kdtree_type(points, compact_nodes=False,
                     balanced_tree=False).query(points, k=5)[-1]
    assert_array_equal(T1, T2)
    assert_array_equal(T1, T3)
    assert_array_equal(T1, T4)

