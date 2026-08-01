
def test_chi_squared():
    k = Symbol("k", integer=True)
    X = ChiSquared('x', k)

    # Tests the characteristic function
    assert characteristic_function(X)(x) == ((-2*I*x + 1)**(-k/2))

    assert density(X)(x) == 2**(-k/2)*x**(k/2 - 1)*exp(-x/2)/gamma(k/2)
    assert cdf(X)(x) == Piecewise((lowergamma(k/2, x/2)/gamma(k/2), x >= 0), (0, True))
    assert E(X) == k
    assert variance(X) == 2*k

    X = ChiSquared('x', 15)
    assert cdf(X)(3) == -14873*sqrt(6)*exp(Rational(-3, 2))/(5005*sqrt(pi)) + erf(sqrt(6)/2)

    k = Symbol("k", integer=True, positive=False)
    raises(ValueError, lambda: ChiSquared('x', k))

    k = Symbol("k", integer=False, positive=True)
    raises(ValueError, lambda: ChiSquared('x', k))

