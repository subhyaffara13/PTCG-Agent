
def test_levy():
    mu = Symbol("mu", real=True)
    c = Symbol("c", positive=True)

    X = Levy('x', mu, c)
    assert X.pspace.domain.set == Interval(mu, oo)
    assert density(X)(x) == sqrt(c/(2*pi))*exp(-c/(2*(x - mu)))/((x - mu)**(S.One + S.Half))
    assert cdf(X)(x) == erfc(sqrt(c/(2*(x - mu))))

    raises(NotImplementedError, lambda: moment_generating_function(X))
    mu = Symbol("mu", real=False)
    raises(ValueError, lambda: Levy('x',mu,c))

    c = Symbol("c", nonpositive=True)
    raises(ValueError, lambda: Levy('x',mu,c))

    mu = Symbol("mu", real=True)
    raises(ValueError, lambda: Levy('x',mu,c))

