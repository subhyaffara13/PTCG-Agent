
def test_valid_origins1(xp):
    """Regression test for #1311."""
    
    def func(x):
        return xp.mean(x)

    data = xp.asarray([1, 2, 3, 4, 5], dtype=xp.float64)
    assert_raises(ValueError, ndimage.generic_filter, data, func, size=3,
                  origin=2)
    assert_raises(ValueError, ndimage.generic_filter1d, data, func,
                  filter_size=3, origin=2)
    assert_raises(ValueError, ndimage.percentile_filter, data, 0.2, size=3,
                  origin=2)

