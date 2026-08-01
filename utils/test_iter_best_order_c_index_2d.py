
def test_iter_best_order_c_index_2d():
    # The C index should be correct with any reordering

    a = arange(6)
    # 2D C-order
    i = nditer(a.reshape(2, 3), ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [0, 1, 2, 3, 4, 5])
    # 2D Fortran-order
    i = nditer(a.reshape(2, 3).copy(order='F'),
                                    ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [0, 3, 1, 4, 2, 5])
    # 2D reversed C-order
    i = nditer(a.reshape(2, 3)[::-1], ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [3, 4, 5, 0, 1, 2])
    i = nditer(a.reshape(2, 3)[:, ::-1], ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [2, 1, 0, 5, 4, 3])
    i = nditer(a.reshape(2, 3)[::-1, ::-1], ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [5, 4, 3, 2, 1, 0])
    # 2D reversed Fortran-order
    i = nditer(a.reshape(2, 3).copy(order='F')[::-1],
                                    ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [3, 0, 4, 1, 5, 2])
    i = nditer(a.reshape(2, 3).copy(order='F')[:, ::-1],
                                    ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [2, 5, 1, 4, 0, 3])
    i = nditer(a.reshape(2, 3).copy(order='F')[::-1, ::-1],
                                    ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [5, 2, 4, 1, 3, 0])

