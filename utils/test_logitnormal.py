
def test_logitnormal():
    mu = Symbol('mu', real=True)
    s = Symbol('s', positive=True)
    X = LogitNormal('x', mu, s)
    x = Symbol('x')

    assert density(X)(x) == sqrt(2)*exp(-(-mu + log(x/(1 - x)))**2/(2*s**2))/(2*sqrt(pi)*s*x*(1 - x))
    assert cdf(X)(x) == erf(sqrt(2)*(-mu + log(x/(1 - x)))/(2*s))/2 + S(1)/2

