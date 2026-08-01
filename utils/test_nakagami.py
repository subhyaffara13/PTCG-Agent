
def test_nakagami():
    mu = Symbol("mu", positive=True)
    omega = Symbol("omega", positive=True)

    X = Nakagami('x', mu, omega)
    assert density(X)(x) == (2*x**(2*mu - 1)*mu**mu*omega**(-mu)
                                *exp(-x**2*mu/omega)/gamma(mu))
    assert simplify(E(X)) == (sqrt(mu)*sqrt(omega)
                                            *gamma(mu + S.Half)/gamma(mu + 1))
    assert simplify(variance(X)) == (
    omega - omega*gamma(mu + S.Half)**2/(gamma(mu)*gamma(mu + 1)))
    assert cdf(X)(x) == Piecewise(
                                (lowergamma(mu, mu*x**2/omega)/gamma(mu), x > 0),
                                (0, True))
    X = Nakagami('x', 1, 1)
    assert median(X) == FiniteSet(sqrt(log(2)))

