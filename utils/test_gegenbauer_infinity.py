
def test_gegenbauer_infinity(n, alpha, x):
    # gh-11713 - check correct handling of x = +inf and x = -inf
    if alpha == 0.0:
        expected = 0.0
    elif n == 0.0:
        expected = 1.0
    else:
        # sign of leading coefficient: 2^n * Gamma(n+alpha) / (n! Gamma(alpha))
        lead_sign = gammasgn(n + alpha) * gammasgn(alpha)
        expected = lead_sign * (np.sign(x) ** n) * np.inf
    assert_allclose(_ufuncs.eval_gegenbauer(int(n), alpha, x), expected, rtol=1e-10)
    assert_allclose(_ufuncs.eval_gegenbauer(float(n), alpha, x), expected, rtol=1e-10)

