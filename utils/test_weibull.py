
def test_weibull():
    a, b = symbols('a b', positive=True)
    # FIXME: simplify(E(X)) seems to hang without extended_positive=True
    # On a Linux machine this had a rapid memory leak...
    # a, b = symbols('a b', positive=True)
    X = Weibull('x', a, b)

    assert E(X).expand() == a * gamma(1 + 1/b)
    assert variance(X).expand() == (a**2 * gamma(1 + 2/b) - E(X)**2).expand()
    assert simplify(skewness(X)) == (2*gamma(1 + 1/b)**3 - 3*gamma(1 + 1/b)*gamma(1 + 2/b) + gamma(1 + 3/b))/(-gamma(1 + 1/b)**2 + gamma(1 + 2/b))**Rational(3, 2)
    assert simplify(kurtosis(X)) == (-3*gamma(1 + 1/b)**4 +\
        6*gamma(1 + 1/b)**2*gamma(1 + 2/b) - 4*gamma(1 + 1/b)*gamma(1 + 3/b) + gamma(1 + 4/b))/(gamma(1 + 1/b)**2 - gamma(1 + 2/b))**2

