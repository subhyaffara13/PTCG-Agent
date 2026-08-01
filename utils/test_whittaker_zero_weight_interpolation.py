
def test_whittaker_zero_weight_interpolation(missing_value):
    """Test that whittaker interpolates where weights are zero."""
    n = 100
    signal = np.sin(2*np.pi * np.linspace(0, 1, n))
    signal[50:] += 2
    w = np.ones_like(signal)
    signal[40:60] = missing_value  # value does not matter
    w[40:60] = 0
    # Note: interpolation is a polynomial of degree = 2 * order - 1.

    # order = 1 => linear interpolation
    wh = whittaker_henderson(signal, lamb=1, order=1, weights=w)
    interp = np.interp(np.arange(40, 60), [39, 60], [wh.x[39], wh.x[60]])
    assert_allclose(wh.x[40:60], interp, rtol=1e-11)

    # order = 2 => cubic interpolation
    wh = whittaker_henderson(signal, lamb=1, order=2, weights=w)
    poly = np.polynomial.Polynomial.fit(
        x=[38, 39, 60, 61], y=[wh.x[38], wh.x[39], wh.x[60], wh.x[61]], deg=3
    )
    assert_allclose(wh.x[40:60], poly(np.arange(40, 60)), rtol=1e-11)

