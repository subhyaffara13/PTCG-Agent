
def test_weibull_numeric():
    # Test for integers and rationals
    a = 1
    bvals = [S.Half, 1, Rational(3, 2), 5]
    for b in bvals:
        X = Weibull('x', a, b)
        assert simplify(E(X)) == expand_func(a * gamma(1 + 1/S(b)))
        assert simplify(variance(X)) == simplify(
            a**2 * gamma(1 + 2/S(b)) - E(X)**2)

