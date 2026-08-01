
def test_sympy__stats__drv_types__PoissonDistribution():
    from sympy.stats.drv_types import PoissonDistribution
    assert _test_args(PoissonDistribution(1))

