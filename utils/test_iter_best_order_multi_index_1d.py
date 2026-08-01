
def test_iter_best_order_multi_index_1d():
    # The multi-indices should be correct with any reordering

    a = arange(4)
    # 1D order
    i = nditer(a, ['multi_index'], [['readonly']])
    assert_equal(iter_multi_index(i), [(0,), (1,), (2,), (3,)])
    # 1D reversed order
    i = nditer(a[::-1], ['multi_index'], [['readonly']])
    assert_equal(iter_multi_index(i), [(3,), (2,), (1,), (0,)])

