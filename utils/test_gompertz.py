
def test_gompertz():
    b = Symbol("b", positive=True)
    eta = Symbol("eta", positive=True)

    X = Gompertz("x", b, eta)

    assert density(X)(x) == b*eta*exp(eta)*exp(b*x)*exp(-eta*exp(b*x))
    assert cdf(X)(x) == 1 - exp(eta)*exp(-eta*exp(b*x))
    assert diff(cdf(X)(x), x) == density(X)(x)

