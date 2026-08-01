
def test_cauchy():
    x0 = Symbol("x0", real=True)
    gamma = Symbol("gamma", positive=True)
    p = Symbol("p", positive=True)

    X = Cauchy('x', x0, gamma)
    # Tests the characteristic function
    assert characteristic_function(X)(x) == exp(-gamma*Abs(x) + I*x*x0)
    raises(NotImplementedError, lambda: moment_generating_function(X))
    assert density(X)(x) == 1/(pi*gamma*(1 + (x - x0)**2/gamma**2))
    assert diff(cdf(X)(x), x) == density(X)(x)
    assert quantile(X)(p) == gamma*tan(pi*(p - S.Half)) + x0

    x1 = Symbol("x1", real=False)
    raises(ValueError, lambda: Cauchy('x', x1, gamma))
    gamma = Symbol("gamma", nonpositive=True)
    raises(ValueError, lambda: Cauchy('x', x0, gamma))
    assert median(X) == FiniteSet(x0)

