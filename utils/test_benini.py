
def test_benini():
    alpha = Symbol("alpha", positive=True)
    beta = Symbol("beta", positive=True)
    sigma = Symbol("sigma", positive=True)
    X = Benini('x', alpha, beta, sigma)

    assert density(X)(x) == ((alpha/x + 2*beta*log(x/sigma)/x)
                          *exp(-alpha*log(x/sigma) - beta*log(x/sigma)**2))

    assert pspace(X).domain.set == Interval(sigma, oo)
    raises(NotImplementedError, lambda: moment_generating_function(X))
    alpha = Symbol("alpha", nonpositive=True)
    raises(ValueError, lambda: Benini('x', alpha, beta, sigma))

    beta = Symbol("beta", nonpositive=True)
    raises(ValueError, lambda: Benini('x', alpha, beta, sigma))

    alpha = Symbol("alpha", positive=True)
    raises(ValueError, lambda: Benini('x', alpha, beta, sigma))

    beta = Symbol("beta", positive=True)
    sigma = Symbol("sigma", nonpositive=True)
    raises(ValueError, lambda: Benini('x', alpha, beta, sigma))

