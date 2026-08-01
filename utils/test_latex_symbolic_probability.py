
def test_latex_symbolic_probability():
    mu = symbols("mu")
    sigma = symbols("sigma", positive=True)
    X = Normal("X", mu, sigma)
    assert latex(Expectation(X)) == r'\operatorname{E}\left[X\right]'
    assert latex(Variance(X)) == r'\operatorname{Var}\left(X\right)'
    assert latex(Probability(X > 0)) == r'\operatorname{P}\left(X > 0\right)'
    Y = Normal("Y", mu, sigma)
    assert latex(Covariance(X, Y)) == r'\operatorname{Cov}\left(X, Y\right)'

