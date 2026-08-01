
def test_random_parameters():
    mu = Normal('mu', 2, 3)
    meas = Normal('T', mu, 1)
    assert density(meas, evaluate=False)(z)
    assert isinstance(pspace(meas), CompoundPSpace)
    X = Normal('x', [1, 2], [[1, 0], [0, 1]])
    assert isinstance(pspace(X).distribution, MultivariateNormalDistribution)
    assert density(meas)(z).simplify() == sqrt(5)*exp(-z**2/20 + z/5 - S(1)/5)/(10*sqrt(pi))

