
def test_PowerFunction():
    alpha = Symbol("alpha", nonpositive=True)
    a, b = symbols('a, b', real=True)
    raises (ValueError, lambda: PowerFunction('x', alpha, a, b))

    a, b = symbols('a, b', real=False)
    raises (ValueError, lambda: PowerFunction('x', alpha, a, b))

    alpha = Symbol("alpha", positive=True)
    a, b = symbols('a, b', real=True)
    raises (ValueError, lambda: PowerFunction('x', alpha, 5, 2))

    X = PowerFunction('X', 2, a, b)
    assert density(X)(z) == (-2*a + 2*z)/(-a + b)**2
    assert cdf(X)(z) == Piecewise((a**2/(a**2 - 2*a*b + b**2) -
        2*a*z/(a**2 - 2*a*b + b**2) + z**2/(a**2 - 2*a*b + b**2), a <= z), (0, True))

    X = PowerFunction('X', 2, 0, 1)
    assert density(X)(z) == 2*z
    assert cdf(X)(z) == Piecewise((z**2, z >= 0), (0,True))
    assert E(X) == Rational(2,3)
    assert P(X < 0) == 0
    assert P(X < 1) == 1
    assert median(X) == FiniteSet(1/sqrt(2))

