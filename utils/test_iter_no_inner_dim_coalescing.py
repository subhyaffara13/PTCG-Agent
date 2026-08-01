
def test_iter_no_inner_dim_coalescing():
    # Check no_inner iterators whose dimensions may not coalesce completely

    # Skipping the last element in a dimension prevents coalescing
    # with the next-bigger dimension
    a = arange(24).reshape(2, 3, 4)[:, :, :-1]
    i = nditer(a, ['external_loop'], [['readonly']])
    assert_equal(i.ndim, 2)
    assert_equal(i[0].shape, (3,))
    a = arange(24).reshape(2, 3, 4)[:, :-1, :]
    i = nditer(a, ['external_loop'], [['readonly']])
    assert_equal(i.ndim, 2)
    assert_equal(i[0].shape, (8,))
    a = arange(24).reshape(2, 3, 4)[:-1, :, :]
    i = nditer(a, ['external_loop'], [['readonly']])
    assert_equal(i.ndim, 1)
    assert_equal(i[0].shape, (12,))

    # Even with lots of 1-sized dimensions, should still coalesce
    a = arange(24).reshape(1, 1, 2, 1, 1, 3, 1, 1, 4, 1, 1)
    i = nditer(a, ['external_loop'], [['readonly']])
    assert_equal(i.ndim, 1)
    assert_equal(i[0].shape, (24,))

