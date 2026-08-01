
def test_masked_array_no_copy():
    # check nomask array is updated in place
    a = np.ma.array([1, 2, 3, 4])
    _ = np.ma.masked_where(a == 3, a, copy=False)
    assert_array_equal(a.mask, [False, False, True, False])
    # check masked array is updated in place
    a = np.ma.array([1, 2, 3, 4], mask=[1, 0, 0, 0])
    _ = np.ma.masked_where(a == 3, a, copy=False)
    assert_array_equal(a.mask, [True, False, True, False])
    # check masked array with masked_invalid is updated in place
    a = np.ma.array([np.inf, 1, 2, 3, 4])
    _ = np.ma.masked_invalid(a, copy=False)
    assert_array_equal(a.mask, [True, False, False, False, False])

