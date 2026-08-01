
def test_sg_coeffs_exact(xp):
    polyorder = 4
    window_length = 9
    halflen = window_length // 2

    x = xp.linspace(0, 21, 43)
    delta = x[1] - x[0]

    # The data is a cubic polynomial.  We'll use an order 4
    # SG filter, so the filtered values should equal the input data
    # (except within half window_length of the edges).
    y = 0.5 * x ** 3 - x
    h = savgol_coeffs(window_length, polyorder, xp=xp)
    y0 = xp.asarray(convolve1d(_xp_copy_to_numpy(y), _xp_copy_to_numpy(h)))
    xp_assert_close(y0[halflen:-halflen], y[halflen:-halflen])

    # Check the same input, but use deriv=1.  dy is the exact result.
    dy = 1.5 * x ** 2 - 1
    h = savgol_coeffs(window_length, polyorder, deriv=1, delta=delta, xp=xp)
    y1 = xp.asarray(convolve1d(_xp_copy_to_numpy(y), _xp_copy_to_numpy(h)))
    xp_assert_close(y1[halflen:-halflen], dy[halflen:-halflen])

    # Check the same input, but use deriv=2. d2y is the exact result.
    d2y = 3.0 * x
    h = savgol_coeffs(window_length, polyorder, deriv=2, delta=delta, xp=xp)
    y2 = xp.asarray(convolve1d(_xp_copy_to_numpy(y), _xp_copy_to_numpy(h)))
    xp_assert_close(y2[halflen:-halflen], d2y[halflen:-halflen])

