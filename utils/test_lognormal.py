
def test_lognormal():
    mean = Symbol('mu', real=True)
    std = Symbol('sigma', positive=True)
    X = LogNormal('x', mean, std)
    # The sympy integrator can't do this too well
    #assert E(X) == exp(mean+std**2/2)
    #assert variance(X) == (exp(std**2)-1) * exp(2*mean + std**2)

    # The sympy integrator can't do this too well
    #assert E(X) ==
    raises(NotImplementedError, lambda: moment_generating_function(X))
    mu = Symbol("mu", real=True)
    sigma = Symbol("sigma", positive=True)

    X = LogNormal('x', mu, sigma)
    assert density(X)(x) == (sqrt(2)*exp(-(-mu + log(x))**2
                                    /(2*sigma**2))/(2*x*sqrt(pi)*sigma))
    # Tests cdf
    assert cdf(X)(x) == Piecewise(
                        (erf(sqrt(2)*(-mu + log(x))/(2*sigma))/2
                        + S(1)/2, x > 0), (0, True))

    X = LogNormal('x', 0, 1)  # Mean 0, standard deviation 1
    assert density(X)(x) == sqrt(2)*exp(-log(x)**2/2)/(2*x*sqrt(pi))

