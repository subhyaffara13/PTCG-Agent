
def test_BoundedPareto():
    L, H = symbols('L, H', negative=True)
    raises(ValueError, lambda: BoundedPareto('X', 1, L, H))
    L, H = symbols('L, H', real=False)
    raises(ValueError, lambda: BoundedPareto('X', 1, L, H))
    L, H = symbols('L, H', positive=True)
    raises(ValueError, lambda: BoundedPareto('X', -1, L, H))

    X = BoundedPareto('X', 2, L, H)
    assert X.pspace.domain.set == Interval(L, H)
    assert density(X)(x) == 2*L**2/(x**3*(1 - L**2/H**2))
    assert cdf(X)(x) == Piecewise((-H**2*L**2/(x**2*(H**2 - L**2)) \
                            + H**2/(H**2 - L**2), L <= x), (0, True))
    assert E(X).simplify() == 2*H*L/(H + L)
    X = BoundedPareto('X', 1, 2, 4)
    assert E(X).simplify() == log(16)
    assert median(X) == FiniteSet(Rational(8, 3))
    assert variance(X).simplify() == 8 - 16*log(2)**2

