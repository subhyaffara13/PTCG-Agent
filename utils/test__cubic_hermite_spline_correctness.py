
def test_CubicHermiteSpline_correctness(xp):
    x = xp.asarray([0, 2, 7])
    y = xp.asarray([-1, 2, 3])
    dydx = xp.asarray([0, 3, 7])
    s = CubicHermiteSpline(x, y, dydx)
    xp_assert_close(s(x), y, check_shape=False, check_dtype=False, rtol=1e-15)
    xp_assert_close(s(x, 1), dydx, check_shape=False, check_dtype=False, rtol=1e-15)

