
def test_sympy__stats__compound_rv__CompoundDistribution():
    from sympy.stats.compound_rv import CompoundDistribution
    from sympy.stats.drv_types import PoissonDistribution, Poisson
    r = Poisson('r', 10)
    assert _test_args(CompoundDistribution(PoissonDistribution(r)))

