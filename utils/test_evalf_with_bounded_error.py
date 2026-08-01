
def test_evalf_with_bounded_error():
    cases = [
        # zero
        (Rational(0), None, 1),
        # zero im part
        (pi, None, 10),
        # zero real part
        (pi*I, None, 10),
        # re and im nonzero
        (2-3*I, None, 5),
        # similar tests again, but using eps instead of m
        (Rational(0), Rational(1, 2), None),
        (pi, Rational(1, 1000), None),
        (pi * I, Rational(1, 1000), None),
        (2 - 3 * I, Rational(1, 1000), None),
        # very large eps
        (2 - 3 * I, Rational(1000), None),
        # case where x already small, hence some cancellation in p = m + n - 1
        (Rational(1234, 10**8), Rational(1, 10**12), None),
    ]
    for x0, eps, m in cases:
        a, b, _, _ = evalf(x0, 53, {})
        c, d, _, _ = _evalf_with_bounded_error(x0, eps, m)
        if eps is None:
            eps = 2**(-m)
        z = make_mpc((a or fzero, b or fzero))
        w = make_mpc((c or fzero, d or fzero))
        assert abs(w - z) < eps

    # eps must be positive
    raises(ValueError, lambda: _evalf_with_bounded_error(pi, Rational(0)))
    raises(ValueError, lambda: _evalf_with_bounded_error(pi, -pi))
    raises(ValueError, lambda: _evalf_with_bounded_error(pi, I))

