
def test_len0_arrays(kdtree_type):
    # make sure len-0 arrays are handled correctly
    # in range queries (gh-5639)
    rng = np.random.RandomState(1234)
    X = rng.rand(10, 2)
    Y = rng.rand(10, 2)
    tree = kdtree_type(X)
    # query_ball_point (single)
    d, i = tree.query([.5, .5], k=1)
    z = tree.query_ball_point([.5, .5], 0.1*d)
    assert_array_equal(z, [])
    # query_ball_point (multiple)
    d, i = tree.query(Y, k=1)
    mind = d.min()
    z = tree.query_ball_point(Y, 0.1*mind)
    y = np.empty(shape=(10, ), dtype=object)
    y.fill([])
    assert_array_equal(y, z)
    # query_ball_tree
    other = kdtree_type(Y)
    y = tree.query_ball_tree(other, 0.1*mind)
    assert_array_equal(10*[[]], y)
    # count_neighbors
    y = tree.count_neighbors(other, 0.1*mind)
    assert_(y == 0)
    # sparse_distance_matrix
    y = tree.sparse_distance_matrix(other, 0.1*mind, output_type='dok_array')
    assert_array_equal(y == np.zeros((10, 10)), True)
    y = tree.sparse_distance_matrix(other, 0.1*mind, output_type='coo_array')
    assert_array_equal(y == np.zeros((10, 10)), True)
    y = tree.sparse_distance_matrix(other, 0.1*mind, output_type='dict')
    assert_equal(y, {})
    y = tree.sparse_distance_matrix(other, 0.1*mind, output_type='ndarray')
    _dtype = [('i', np.intp), ('j', np.intp), ('v', np.float64)]
    res_dtype = np.dtype(_dtype, align=True)
    z = np.empty(shape=(0, ), dtype=res_dtype)
    assert_array_equal(y, z)
    # query_pairs
    d, i = tree.query(X, k=2)
    mind = d[:, -1].min()
    y = tree.query_pairs(0.1*mind, output_type='set')
    assert_equal(y, set())
    y = tree.query_pairs(0.1*mind, output_type='ndarray')
    z = np.empty(shape=(0, 2), dtype=np.intp)
    assert_array_equal(y, z)

