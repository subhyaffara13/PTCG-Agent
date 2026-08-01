
def test_sg_filter_interp_edges(xp):
    # Another test with low degree polynomial data, for which we can easily
    # give the exact results. In this test, we use mode='interp', so
    # savgol_filter should match the exact solution for the entire data set,
    # including the edges.
    t = xp.linspace(-5, 5, 21, dtype=xp.float64)
    delta = t[1] - t[0]
    # Polynomial test data.
    x = xp.stack([t,
                  3 * t ** 2,
                  t ** 3 - t])
    dx = xp.stack([xp.ones_like(t),
                   6 * t,
                   3 * t ** 2 - 1.0])
    d2x = xp.stack([xp.zeros_like(t),
                    xp.full_like(t, 6),
                    6 * t])

    window_length = 7

    y = savgol_filter(x, window_length, 3, axis=-1, mode='interp')
    xp_assert_close(y, x, atol=1e-12)

    y1 = savgol_filter(x, window_length, 3, axis=-1, mode='interp',
                       deriv=1, delta=delta)
    xp_assert_close(y1, dx, atol=1e-12)

    y2 = savgol_filter(x, window_length, 3, axis=-1, mode='interp',
                       deriv=2, delta=delta)
    xp_assert_close(y2, d2x, atol=1e-12)

    # Transpose everything, and test again with axis=0.

    x = x.T
    dx = dx.T
    d2x = d2x.T

    y = savgol_filter(x, window_length, 3, axis=0, mode='interp')
    xp_assert_close(y, x, atol=1e-12)

    y1 = savgol_filter(x, window_length, 3, axis=0, mode='interp',
                       deriv=1, delta=delta)
    xp_assert_close(y1, dx, atol=1e-12)

    y2 = savgol_filter(x, window_length, 3, axis=0, mode='interp',
                       deriv=2, delta=delta)
    xp_assert_close(y2, d2x, atol=1e-12)

