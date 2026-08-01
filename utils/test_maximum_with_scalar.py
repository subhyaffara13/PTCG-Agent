
def test_maximum_with_scalar():
    a = coo_array([0,1,6])
    b = coo_array([[15, 0], [14, 5], [0, -12]])
    c = coo_array([[[[3,0], [2,4]], [[8,9], [-3,12]]],
                   [[[5,2], [3,0]], [[0,7], [0,-6]]]])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SparseEfficiencyWarning)
        assert_equal(a.maximum(5).toarray(), np.maximum(a.toarray(), 5))
        assert_equal(b.maximum(9).toarray(), np.maximum(b.toarray(), 9))
        assert_equal(c.maximum(5).toarray(), np.maximum(c.toarray(), 5))

