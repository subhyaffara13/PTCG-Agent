
def test_sg_filter_trivial(xp):
    """ Test some trivial edge cases for savgol_filter()."""
    x = xp.asarray([1.0])
    y = savgol_filter(x, 1, 0)
    xp_assert_equal(y, xp.asarray([1.0]))

    # Input is a single value. With a window length of 3 and polyorder 1,
    # the value in y is from the straight-line fit of (-1,0), (0,3) and
    # (1, 0) at 0. This is just the average of the three values, hence 1.0.
    x = xp.asarray([3.0])
    y = savgol_filter(x, 3, 1, mode='constant')
    xp_assert_close(y, xp.asarray([1.0]), atol=1.5e-15)

    x = xp.asarray([3.0])
    y = savgol_filter(x, 3, 1, mode='nearest')
    xp_assert_close(y, xp.asarray([3.0]), atol=1.5e-15)

    x = xp.asarray([1.0] * 3)
    y = savgol_filter(x, 3, 1, mode='wrap')
    xp_assert_close(y, xp.asarray([1.0, 1.0, 1.0]), atol=1.5e-15)

