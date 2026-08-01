
def test_maxwell():
    a = Symbol("a", positive=True)

    X = Maxwell('x', a)

    assert density(X)(x) == (sqrt(2)*x**2*exp(-x**2/(2*a**2))/
        (sqrt(pi)*a**3))
    assert E(X) == 2*sqrt(2)*a/sqrt(pi)
    assert variance(X) == -8*a**2/pi + 3*a**2
    assert cdf(X)(x) == erf(sqrt(2)*x/(2*a)) - sqrt(2)*x*exp(-x**2/(2*a**2))/(sqrt(pi)*a)
    assert diff(cdf(X)(x), x) == density(X)(x)

