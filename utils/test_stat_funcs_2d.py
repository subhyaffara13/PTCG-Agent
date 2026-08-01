
def test_stat_funcs_2d(xp):
    a = xp.asarray([[5, 6, 0, 0, 0], [8, 9, 0, 0, 0], [0, 0, 0, 3, 5]])
    lbl = xp.asarray([[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 2, 2]])

    mean = ndimage.mean(a, labels=lbl, index=xp.asarray([1, 2]))
    xp_assert_equal(mean, xp.asarray([7.0, 4.0], dtype=xp.float64))

    var = ndimage.variance(a, labels=lbl, index=xp.asarray([1, 2]))
    xp_assert_equal(var, xp.asarray([2.5, 1.0], dtype=xp.float64))

    std = ndimage.standard_deviation(a, labels=lbl, index=xp.asarray([1, 2]))
    assert_array_almost_equal(std, xp.sqrt(xp.asarray([2.5, 1.0], dtype=xp.float64)))

    med = ndimage.median(a, labels=lbl, index=xp.asarray([1, 2]))
    xp_assert_equal(med, xp.asarray([7.0, 4.0], dtype=xp.float64))

    min = ndimage.minimum(a, labels=lbl, index=xp.asarray([1, 2]))
    xp_assert_equal(min, xp.asarray([5, 3]), check_dtype=False)

    max = ndimage.maximum(a, labels=lbl, index=xp.asarray([1, 2]))
    xp_assert_equal(max, xp.asarray([9, 5]), check_dtype=False)

