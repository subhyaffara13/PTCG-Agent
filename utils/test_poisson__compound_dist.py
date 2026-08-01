
def test_poisson_CompoundDist():
    k, t, y = symbols('k t y', positive=True, real=True)
    G = Gamma('G', k, t)
    D = Poisson('P', G)
    assert density(D)(y).simplify() == t**y*(t + 1)**(-k - y)*gamma(k + y)/(gamma(k)*gamma(y + 1))
    # https://en.wikipedia.org/wiki/Negative_binomial_distribution#Gamma%E2%80%93Poisson_mixture
    assert E(D).simplify() == k*t # mean of NegativeBinomialDistribution

