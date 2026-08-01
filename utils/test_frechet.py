
def test_frechet():
    a = Symbol("a", positive=True)
    s = Symbol("s", positive=True)
    m = Symbol("m", real=True)

    X = Frechet("x", a, s=s, m=m)
    assert density(X)(x) == a*((x - m)/s)**(-a - 1)*exp(-((x - m)/s)**(-a))/s
    assert cdf(X)(x) == Piecewise((exp(-((-m + x)/s)**(-a)), m <= x), (0, True))

