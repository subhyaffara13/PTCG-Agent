
def test_Moyal():
    mu = Symbol('mu',real=False)
    sigma = Symbol('sigma', positive=True)
    raises(ValueError, lambda: Moyal('M',mu, sigma))

    mu = Symbol('mu', real=True)
    sigma = Symbol('sigma', negative=True)
    raises(ValueError, lambda: Moyal('M',mu, sigma))

    sigma = Symbol('sigma', positive=True)
    M = Moyal('M', mu, sigma)
    assert density(M)(z) == sqrt(2)*exp(-exp((mu - z)/sigma)/2
                        - (-mu + z)/(2*sigma))/(2*sqrt(pi)*sigma)
    assert cdf(M)(z).simplify() == 1 - erf(sqrt(2)*exp((mu - z)/(2*sigma))/2)
    assert characteristic_function(M)(z) == 2**(-I*sigma*z)*exp(I*mu*z) \
                        *gamma(-I*sigma*z + Rational(1, 2))/sqrt(pi)
    assert E(M) == mu + EulerGamma*sigma + sigma*log(2)
    assert moment_generating_function(M)(z) == 2**(-sigma*z)*exp(mu*z) \
                        *gamma(-sigma*z + Rational(1, 2))/sqrt(pi)

