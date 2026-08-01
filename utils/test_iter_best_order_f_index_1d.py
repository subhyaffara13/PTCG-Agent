
def test_iter_best_order_f_index_1d():
    # The Fortran index should be correct with any reordering

    a = arange(4)
    # 1D order
    i = nditer(a, ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [0, 1, 2, 3])
    # 1D reversed order
    i = nditer(a[::-1], ['f_index'], [['readonly']])
    assert_equal(iter_indices(i), [3, 2, 1, 0])

