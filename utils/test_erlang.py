
def test_erlang():
    k = Symbol("k", integer=True, positive=True)
    l = Symbol("l", positive=True)

    X = Erlang("x", k, l)
    assert density(X)(x) == x**(k - 1)*l**k*exp(-x*l)/gamma(k)
    assert cdf(X)(x) == Piecewise((lowergamma(k, l*x)/gamma(k), x > 0),
                               (0, True))

