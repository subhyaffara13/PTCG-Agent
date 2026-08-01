
def test_loglogistic():
    a, b = symbols('a b')
    assert LogLogistic('x', a, b)

    a = Symbol('a', negative=True)
    b = Symbol('b', positive=True)
    raises(ValueError, lambda: LogLogistic('x', a, b))

    a = Symbol('a', positive=True)
    b = Symbol('b', negative=True)
    raises(ValueError, lambda: LogLogistic('x', a, b))

    a, b, z, p = symbols('a b z p', positive=True)
    X = LogLogistic('x', a, b)
    assert density(X)(z) == b*(z/a)**(b - 1)/(a*((z/a)**b + 1)**2)
    assert cdf(X)(z) == 1/(1 + (z/a)**(-b))
    assert quantile(X)(p) == a*(p/(1 - p))**(1/b)

    # Expectation
    assert E(X) == Piecewise((S.NaN, b <= 1), (pi*a/(b*sin(pi/b)), True))
    b = symbols('b', prime=True) # b > 1
    X = LogLogistic('x', a, b)
    assert E(X) == pi*a/(b*sin(pi/b))
    X = LogLogistic('x', 1, 2)
    assert median(X) == FiniteSet(1)

