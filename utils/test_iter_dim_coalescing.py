
def test_iter_dim_coalescing():
    # Check that the correct number of dimensions are coalesced

    # Tracking a multi-index disables coalescing
    a = arange(24).reshape(2, 3, 4)
    i = nditer(a, ['multi_index'], [['readonly']])
    assert_equal(i.ndim, 3)

    # A tracked index can allow coalescing if it's compatible with the array
    a3d = arange(24).reshape(2, 3, 4)
    i = nditer(a3d, ['c_index'], [['readonly']])
    assert_equal(i.ndim, 1)
    i = nditer(a3d.swapaxes(0, 1), ['c_index'], [['readonly']])
    assert_equal(i.ndim, 3)
    i = nditer(a3d.T, ['c_index'], [['readonly']])
    assert_equal(i.ndim, 3)
    i = nditer(a3d.T, ['f_index'], [['readonly']])
    assert_equal(i.ndim, 1)
    i = nditer(a3d.T.swapaxes(0, 1), ['f_index'], [['readonly']])
    assert_equal(i.ndim, 3)

    # When C or F order is forced, coalescing may still occur
    a3d = arange(24).reshape(2, 3, 4)
    i = nditer(a3d, order='C')
    assert_equal(i.ndim, 1)
    i = nditer(a3d.T, order='C')
    assert_equal(i.ndim, 3)
    i = nditer(a3d, order='F')
    assert_equal(i.ndim, 3)
    i = nditer(a3d.T, order='F')
    assert_equal(i.ndim, 1)
    i = nditer(a3d, order='A')
    assert_equal(i.ndim, 1)
    i = nditer(a3d.T, order='A')
    assert_equal(i.ndim, 1)

