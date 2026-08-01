
def test_symbolic_probability():
    mu = symbols("mu")
    sigma = symbols("sigma", positive=True)
    X = Normal("X", mu, sigma)
    assert pretty(Expectation(X)) == r'E[X]'
    assert pretty(Variance(X)) == r'Var(X)'
    assert pretty(Probability(X > 0)) == r'P(X > 0)'
    Y = Normal("Y", mu, sigma)
    assert pretty(Covariance(X, Y)) == 'Cov(X, Y)'

