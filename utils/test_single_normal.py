
def test_single_normal():
    mu = Symbol('mu', real=True)
    sigma = Symbol('sigma', positive=True)
    X = Normal('x', 0, 1)
    Y = X*sigma + mu

    assert E(Y) == mu
    assert variance(Y) == sigma**2
    pdf = density(Y)
    x = Symbol('x', real=True)
    assert (pdf(x) ==
            2**S.Half*exp(-(x - mu)**2/(2*sigma**2))/(2*pi**S.Half*sigma))

    assert P(X**2 < 1) == erf(2**S.Half/2)
    ans = quantile(Y)(x)
    assert ans == Complement(Intersection(FiniteSet(
        sqrt(2)*sigma*(sqrt(2)*mu/(2*sigma)+ erfinv(2*x - 1))),
        Interval(-oo, oo)), FiniteSet(mu))
    assert E(X, Eq(X, mu)) == mu

    assert median(X) == FiniteSet(0)
    # issue 8248
    assert X.pspace.compute_expectation(1).doit() == 1

