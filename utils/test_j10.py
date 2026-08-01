
def test_J10():
    mu, nu = symbols('mu, nu', integer=True)
    assert assoc_legendre(nu, mu, 0) == 2**mu*sqrt(pi)/gamma((nu - mu)/2 + 1)/gamma((-nu - mu + 1)/2)

