
def test_exponential_power():
    mu = Symbol('mu')
    z = Symbol('z')
    alpha = Symbol('alpha', positive=True)
    beta = Symbol('beta', positive=True)

    X = ExponentialPower('x', mu, alpha, beta)

    assert density(X)(z) == beta*exp(-(Abs(mu - z)/alpha)
                                     ** beta)/(2*alpha*gamma(1/beta))
    assert cdf(X)(z) == S.Half + lowergamma(1/beta,
                            (Abs(mu - z)/alpha)**beta)*sign(-mu + z)/\
                                (2*gamma(1/beta))

