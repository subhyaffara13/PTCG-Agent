
def test_sg_filter_basic(xp):
    # Some basic test cases for savgol_filter().
    x = xp.asarray([1.0, 2.0, 1.0])
    y = savgol_filter(x, 3, 1, mode='constant')
    xp_assert_close(y, xp.asarray([1.0, 4.0 / 3, 1.0]))

    y = savgol_filter(x, 3, 1, mode='mirror')
    xp_assert_close(y, xp.asarray([5.0 / 3, 4.0 / 3, 5.0 / 3]))

    y = savgol_filter(x, 3, 1, mode='wrap')
    xp_assert_close(y, xp.asarray([4.0 / 3, 4.0 / 3, 4.0 / 3]))

