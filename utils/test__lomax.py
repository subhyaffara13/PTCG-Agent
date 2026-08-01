
def test_Lomax():
    a, l = symbols('a, l', negative=True)
    raises(ValueError, lambda: Lomax('X', a, l))
    a, l = symbols('a, l', real=False)
    raises(ValueError, lambda: Lomax('X', a, l))

    a, l = symbols('a, l', positive=True)
    X = Lomax('X', a, l)
    assert X.pspace.domain.set == Interval(0, oo)
    assert density(X)(x) == a*(1 + x/l)**(-a - 1)/l
    assert cdf(X)(x) == Piecewise((1 - (1 + x/l)**(-a), x >= 0), (0, True))
    a = 3
    X = Lomax('X', a, l)
    assert E(X) == l/2
    assert median(X) == FiniteSet(l*(-1 + 2**Rational(1, 3)))
    assert variance(X) == 3*l**2/4

