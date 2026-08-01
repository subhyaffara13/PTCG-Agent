
def test_kdtree_attributes():
    # Test KDTree's attributes are available
    np.random.seed(1234)
    points = np.random.rand(100, 4)
    t = KDTree(points)

    assert isinstance(t.m, int)
    assert t.n == points.shape[0]

    assert isinstance(t.n, int)
    assert t.m == points.shape[1]

    assert isinstance(t.leafsize, int)
    assert t.leafsize == 10

    assert_array_equal(t.maxes, np.amax(points, axis=0))
    assert_array_equal(t.mins, np.amin(points, axis=0))
    assert t.data.base is points

