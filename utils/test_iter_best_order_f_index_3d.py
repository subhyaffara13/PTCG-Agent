
def test_iter_best_order_f_index_3d():
    # The Fortran index should be correct with any reordering

    a = arange(12)
    # 3D C-order
    i = nditer(a.reshape(2, 3, 2), ['f_index'], [['readonly']])
    assert_equal(iter_indices(i),
                            [0, 6, 2, 8, 4, 10, 1, 7, 3, 9, 5, 11])
    # 3D Fortran-order
    i = nditer(a.reshape(2, 3, 2).copy(order='F'),
                                    ['f_index'], [['readonly']])
    assert_equal(iter_indices(i),
                            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    # 3D reversed C-order
    i = nditer(a.reshape(2, 3, 2)[::-1], ['f_index'], [['readonly']])
    assert_equal(iter_indices(i),
                            [1, 7, 3, 9, 5, 11, 0, 6, 2, 8, 4, 10])
    i = nditer(a.reshape(2, 3, 2)[:, ::-1], ['f_index'], [['readonly']])
    assert_equal(iter_indices(i),
                            [4, 10, 2, 8, 0, 6, 5, 11, 3, 9, 1, 7])
    i = nditer(a.reshape(2, 3, 2)[:, :, ::-1], ['f_index'], [['readonly']])
    assert_equal(iter_indices(i),
                            [6, 0, 8, 2, 10, 4, 7, 1, 9, 3, 11, 5])
    # 3D reversed Fortran-order
    i = nditer(a.reshape(2, 3, 2).copy(order='F')[::-1],
                                    ['f_index'], [['readonly']])
    assert_equal(iter_indices(i),
                            [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10])
    i = nditer(a.reshape(2, 3, 2).copy(order='F')[:, ::-1],
                                    ['f_index'], [['readonly']])
    assert_equal(iter_indices(i),
                            [4, 5, 2, 3, 0, 1, 10, 11, 8, 9, 6, 7])
    i = nditer(a.reshape(2, 3, 2).copy(order='F')[:, :, ::-1],
                                    ['f_index'], [['readonly']])
    assert_equal(iter_indices(i),
                            [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5])

