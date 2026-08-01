
def test_iter_best_order_c_index_1d():
    # The C index should be correct with any reordering

    a = arange(4)
    # 1D order
    i = nditer(a, ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [0, 1, 2, 3])
    # 1D reversed order
    i = nditer(a[::-1], ['c_index'], [['readonly']])
    assert_equal(iter_indices(i), [3, 2, 1, 0])

