
def test_iter_remove_multi_index_inner_loop():
    # Check that removing multi-index support works

    a = arange(24).reshape(2, 3, 4)

    i = nditer(a, ['multi_index'])
    assert_equal(i.ndim, 3)
    assert_equal(i.shape, (2, 3, 4))
    assert_equal(i.itviews[0].shape, (2, 3, 4))

    # Removing the multi-index tracking causes all dimensions to coalesce
    before = list(i)
    i.remove_multi_index()
    after = list(i)

    assert_equal(before, after)
    assert_equal(i.ndim, 1)
    assert_raises(ValueError, lambda i: i.shape, i)
    assert_equal(i.itviews[0].shape, (24,))

    # Removing the inner loop means there's just one iteration
    i.reset()
    assert_equal(i.itersize, 24)
    assert_equal(i[0].shape, ())
    i.enable_external_loop()
    assert_equal(i.itersize, 24)
    assert_equal(i[0].shape, (24,))
    assert_equal(i.value, arange(24))

