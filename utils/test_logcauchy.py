
def test_logcauchy():
    mu = Symbol("mu", positive=True)
    sigma = Symbol("sigma", positive=True)

    X = LogCauchy("x", mu, sigma)

    assert density(X)(x) == sigma/(x*pi*(sigma**2 + (-mu + log(x))**2))
    assert cdf(X)(x) == atan((log(x) - mu)/sigma)/pi + S.Half

