
def test_compound_distribution():
    Y = Poisson('Y', 1)
    Z = Poisson('Z', Y)
    assert isinstance(pspace(Z), CompoundPSpace)
    assert isinstance(pspace(Z).distribution, CompoundDistribution)
    assert Z.pspace.distribution.pdf(1).doit() == exp(-2)*exp(exp(-1))

