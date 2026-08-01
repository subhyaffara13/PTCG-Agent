
def test_whittaker_limit_infinity_penalty(weights, order):
    """Test whittaker for penalty lamb close to infinity."""
    n = 100
    y = np.sin(2*np.pi * np.linspace(0, 1, n))
    w = None if weights is None else np.ones_like(y)

    # In the limit of an infinite penalty, the smoothing results in an interpolation
    # polynom of degree = penalty order - 1 (order=2 => linear)
    wh = whittaker_henderson(y, lamb=1e11, order=order, weights=w)
    x_poly = np.arange(len(y))
    poly = np.polynomial.Polynomial.fit(x=x_poly, y=y, deg=order - 1)
    assert_allclose(wh.x, poly(x_poly), rtol=10**(-6 + order), atol=1e-5)
    if order == 2:
        # Linear interpolation:
        # As the sine is positive fom 0 to pi and negative from pi to 2*pi, we expect
        # a negative slope.
        assert np.diff(wh.x)[0] < 0

    if order > 2:
        # Very large lambda should trigger a user warning and produce the exact
        # polynomial fit (separate code path where linear solver breaks down).
        with pytest.warns(
            UserWarning,
            match="The linear solver in Whittaker-Henderson smoothing detected",
        ):
            wh = whittaker_henderson(y, lamb=1e15, order=order, weights=w)
    else:
        wh = whittaker_henderson(y, lamb=1e20, order=order, weights=w)
    assert_allclose(wh.x, poly(x_poly), rtol=1e-10)

