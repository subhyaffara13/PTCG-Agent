
def test_sympy__stats__compound_rv__CompoundPSpace():
    from sympy.stats.compound_rv import CompoundPSpace, CompoundDistribution
    from sympy.stats.drv_types import PoissonDistribution, Poisson
    r = Poisson('r', 5)
    C = CompoundDistribution(PoissonDistribution(r))
    assert _test_args(CompoundPSpace('C', C))

