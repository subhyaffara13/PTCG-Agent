
def test_density():
    x = Symbol('x')
    l = Symbol('l', positive=True)
    rate = Beta(l, 2, 3)
    X = Poisson(x, rate)
    assert isinstance(pspace(X), CompoundPSpace)
    assert density(X, Eq(rate, rate.symbol)) == PoissonDistribution(l)
    N1 = Normal('N1', 0, 1)
    N2 = Normal('N2', N1, 2)
    assert density(N2)(0).doit() == sqrt(10)/(10*sqrt(pi))
    assert simplify(density(N2, Eq(N1, 1))(x)) == \
        sqrt(2)*exp(-(x - 1)**2/8)/(4*sqrt(pi))
    assert simplify(density(N2)(x)) == sqrt(10)*exp(-x**2/10)/(10*sqrt(pi))


def test_density():
    d = Density([Jz*mo, 0.5], [Jz*po, 0.5])
    assert qapply(d) == Density([-hbar*mo, 0.5], [hbar*po, 0.5])

