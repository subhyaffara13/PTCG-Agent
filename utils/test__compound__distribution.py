
def test_Compound_Distribution():
    X = Normal('X', 2, 4)
    N = NormalDistribution(X, 4)
    C = CompoundDistribution(N)
    assert C.is_Continuous
    assert C.set == Interval(-oo, oo)
    assert C.pdf(x, evaluate=True).simplify() == exp(-x**2/64 + x/16 - S(1)/16)/(8*sqrt(pi))

    assert not isinstance(CompoundDistribution(NormalDistribution(2, 3)),
                            CompoundDistribution)
    M = MultivariateNormalDistribution([1, 2], [[2, 1], [1, 2]])
    raises(NotImplementedError, lambda: CompoundDistribution(M))

    X = Beta('X', 2, 4)
    B = BernoulliDistribution(X, 1, 0)
    C = CompoundDistribution(B)
    assert C.is_Finite
    assert C.set == {0, 1}
    y = symbols('y', negative=False, integer=True)
    assert C.pdf(y, evaluate=True) == Piecewise((S(1)/(30*beta(2, 4)), Eq(y, 0)),
                (S(1)/(60*beta(2, 4)), Eq(y, 1)), (0, True))

    k, t, z = symbols('k t z', positive=True, real=True)
    G = Gamma('G', k, t)
    X = PoissonDistribution(G)
    C = CompoundDistribution(X)
    assert C.is_Discrete
    assert C.set == S.Naturals0
    assert C.pdf(z, evaluate=True).simplify() == t**z*(t + 1)**(-k - z)*gamma(k \
                    + z)/(gamma(k)*gamma(z + 1))

