
def test_minmaximum_filter1d(xp):
    # Regression gh-3898
    in_ = xp.arange(10)
    out = ndimage.minimum_filter1d(in_, 1)
    xp_assert_equal(in_, out)
    out = ndimage.maximum_filter1d(in_, 1)
    xp_assert_equal(in_, out)
    # Test reflect
    out = ndimage.minimum_filter1d(in_, 5, mode='reflect')
    xp_assert_equal(xp.asarray([0, 0, 0, 1, 2, 3, 4, 5, 6, 7]), out)
    out = ndimage.maximum_filter1d(in_, 5, mode='reflect')
    xp_assert_equal(xp.asarray([2, 3, 4, 5, 6, 7, 8, 9, 9, 9]), out)
    # Test constant
    out = ndimage.minimum_filter1d(in_, 5, mode='constant', cval=-1)
    xp_assert_equal(xp.asarray([-1, -1, 0, 1, 2, 3, 4, 5, -1, -1]), out)
    out = ndimage.maximum_filter1d(in_, 5, mode='constant', cval=10)
    xp_assert_equal(xp.asarray([10, 10, 4, 5, 6, 7, 8, 9, 10, 10]), out)
    # Test nearest
    out = ndimage.minimum_filter1d(in_, 5, mode='nearest')
    xp_assert_equal(xp.asarray([0, 0, 0, 1, 2, 3, 4, 5, 6, 7]), out)
    out = ndimage.maximum_filter1d(in_, 5, mode='nearest')
    xp_assert_equal(xp.asarray([2, 3, 4, 5, 6, 7, 8, 9, 9, 9]), out)
    # Test wrap
    out = ndimage.minimum_filter1d(in_, 5, mode='wrap')
    xp_assert_equal(xp.asarray([0, 0, 0, 1, 2, 3, 4, 5, 0, 0]), out)
    out = ndimage.maximum_filter1d(in_, 5, mode='wrap')
    xp_assert_equal(xp.asarray([9, 9, 4, 5, 6, 7, 8, 9, 9, 9]), out)

