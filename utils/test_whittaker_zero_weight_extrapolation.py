
def test_whittaker_zero_weight_extrapolation():
    """Test that whittaker extrapolates where weights are zero."""
    n = 100
    signal = np.sin(2*np.pi * np.linspace(0, 1, n))
    signal[50:] += 2
    w = np.ones_like(signal)
    signal[80:] = np.nan  # value does not matter, np.nan to check arg validation
    w[80:] = 0
    # Note: extrapolation is a polynomial of degree = order - 1.

    # order = 1 => constant extrapolation
    wh = whittaker_henderson(signal, lamb=1, order=1, weights=w)
    assert_allclose(wh.x[80:], wh.x[79], rtol=1e-11)

    # order 2 => linear extrapolation
    wh = whittaker_henderson(signal, lamb=1, order=2, weights=w)
    poly = np.polynomial.Polynomial.fit(x=[78, 79], y=wh.x[78:80], deg=1)
    assert_allclose(wh.x[80:], poly(np.arange(80, 100)), rtol=1e-11)

    # order = 3 => quadratic extrapolation
    wh = whittaker_henderson(signal, lamb=1, order=3, weights=w)
    poly = np.polynomial.Polynomial.fit(x=[77, 78, 79], y=wh.x[77:80], deg=2)
    assert_allclose(wh.x[80:], poly(np.arange(80, 100)), rtol=1e-9)

