
def test_sg_coeffs_deriv(xp):
    # The data in `x` is a sampled parabola, so using savgol_coeffs with an
    # order 2 or higher polynomial should give exact results.
    i = xp.asarray([-2.0, 0.0, 2.0, 4.0, 6.0], dtype=xp.float64)
    x = i ** 2 / 4
    dx = i / 2
    d2x = xp.full_like(i, 0.5)
    for pos in range(x.shape[0]):
        coeffs0 = savgol_coeffs(5, 3, pos=pos, delta=2.0, use='dot', xp=xp)
        xp_assert_close(coeffs0 @ x, x[pos], atol=1e-10)
        coeffs1 = savgol_coeffs(5, 3, pos=pos, delta=2.0, use='dot', deriv=1, xp=xp)
        xp_assert_close(coeffs1 @ x, dx[pos], atol=1e-10)
        coeffs2 = savgol_coeffs(5, 3, pos=pos, delta=2.0, use='dot', deriv=2, xp=xp)
        xp_assert_close(coeffs2 @ x , d2x[pos], atol=1e-10)

