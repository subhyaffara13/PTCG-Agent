
def test_gamma_inverse():
    a = Symbol("a", positive=True)
    b = Symbol("b", positive=True)
    X = GammaInverse("x", a, b)
    assert density(X)(x) == x**(-a - 1)*b**a*exp(-b/x)/gamma(a)
    assert cdf(X)(x) == Piecewise((uppergamma(a, b/x)/gamma(a), x > 0), (0, True))
    assert characteristic_function(X)(x) == 2 * (-I*b*x)**(a/2) \
            * besselk(a, 2*sqrt(b)*sqrt(-I*x))/gamma(a)
    raises(NotImplementedError, lambda: moment_generating_function(X))

