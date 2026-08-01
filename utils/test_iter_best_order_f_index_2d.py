
def test_iter_best_order_f_index_2d():
    # The Fortran index should be correct with any reordering

    a = arange(6)
    # 2D C-order
    i = nditer(a.reshape(2, 3), ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [0, 2, 4, 1, 3, 5])
    # 2D Fortran-order
    i = nditer(a.reshape(2, 3).copy(order='F'),
                                    ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [0, 1, 2, 3, 4, 5])
    # 2D reversed C-order
    i = nditer(a.reshape(2, 3)[::-1], ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [1, 3, 5, 0, 2, 4])
    i = nditer(a.reshape(2, 3)[:, ::-1], ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [4, 2, 0, 5, 3, 1])
    i = nditer(a.reshape(2, 3)[::-1, ::-1], ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [5, 3, 1, 4, 2, 0])
    # 2D reversed Fortran-order
    i = nditer(a.reshape(2, 3).copy(order='F')[::-1],
                                    ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [1, 0, 3, 2, 5, 4])
    i = nditer(a.reshape(2, 3).copy(order='F')[:, ::-1],
                                    ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [4, 5, 2, 3, 0, 1])
    i = nditer(a.reshape(2, 3).copy(order='F')[::-1, ::-1],
                                    ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [5, 4, 3, 2, 1, 0])

