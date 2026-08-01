
def test_shape_constructor():
    empty1d = coo_array((3,))
    assert empty1d.shape == (3,)
    assert_equal(empty1d.toarray(), np.zeros((3,)))

    empty2d = coo_array((3, 2))
    assert empty2d.shape == (3, 2)
    assert_equal(empty2d.toarray(), np.zeros((3, 2)))

    empty_nd = coo_array((2,3,4,6,7))
    assert empty_nd.shape == (2,3,4,6,7)
    assert_equal(empty_nd.toarray(), np.zeros((2,3,4,6,7)))

