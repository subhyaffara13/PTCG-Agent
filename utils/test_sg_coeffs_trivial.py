
def test_sg_coeffs_trivial(xp):
    # Test a trivial case of savgol_coeffs: polyorder = window_length - 1
    h = savgol_coeffs(1, 0, xp=xp)
    xp_assert_close(h, xp.asarray([1.0], dtype=xp.float64))

    h = savgol_coeffs(3, 2, xp=xp)
    xp_assert_close(h, xp.asarray([0.0, 1, 0], dtype=xp.float64), atol=1e-10)

    h = savgol_coeffs(5, 4, xp=xp)
    xp_assert_close(h, xp.asarray([0.0, 0, 1, 0, 0], dtype=xp.float64), atol=1e-10)

    h = savgol_coeffs(5, 4, pos=1, xp=xp)
    xp_assert_close(h, xp.asarray([0.0, 0, 0, 1, 0], dtype=xp.float64), atol=1e-10)

    h = savgol_coeffs(5, 4, pos=1, use='dot', xp=xp)
    xp_assert_close(h, xp.asarray([0.0, 1, 0, 0, 0], dtype=xp.float64), atol=1e-10)

