
def test_zero_der_nz_dp(capsys):
    """Test secant method with a non-zero dp, but an infinite newton step"""
    # pick a symmetrical functions and choose a point on the side that with dx
    # makes a secant that is a flat line with zero slope, EG: f = (x - 100)**2,
    # which has a root at x = 100 and is symmetrical around the line x = 100
    # we have to pick a really big number so that it is consistently true
    # now find a point on each side so that the secant has a zero slope
    dx = np.finfo(float).eps ** 0.33
    # 100 - p0 = p1 - 100 = p0 * (1 + dx) + dx - 100
    # -> 200 = p0 * (2 + dx) + dx
    p0 = (200.0 - dx) / (2.0 + dx)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "RMS of", RuntimeWarning)
        x = zeros.newton(lambda y: (y - 100.0)**2, x0=[p0] * 10)
    assert_allclose(x, [100] * 10)
    # test scalar cases too
    p0 = (2.0 - 1e-4) / (2.0 + 1e-4)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "Tolerance of", RuntimeWarning)
        x = zeros.newton(lambda y: (y - 1.0) ** 2, x0=p0, disp=False)
    assert_allclose(x, 1)
    with pytest.raises(RuntimeError, match='Tolerance of'):
        x = zeros.newton(lambda y: (y - 1.0) ** 2, x0=p0, disp=True)
    p0 = (-2.0 + 1e-4) / (2.0 + 1e-4)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "Tolerance of", RuntimeWarning)
        x = zeros.newton(lambda y: (y + 1.0) ** 2, x0=p0, disp=False)
    assert_allclose(x, -1)
    with pytest.raises(RuntimeError, match='Tolerance of'):
        x = zeros.newton(lambda y: (y + 1.0) ** 2, x0=p0, disp=True)

