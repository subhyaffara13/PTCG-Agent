
def test_ellip_harm_invalid_p():
    # Regression test. This should return nan.
    n = 4
    # Make p > 2*n + 1.
    p = 2*n + 2
    result = ellip_harm(0.5, 2.0, n, p, 0.2)
    assert np.isnan(result)

