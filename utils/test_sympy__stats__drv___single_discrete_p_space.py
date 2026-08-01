
def test_sympy__stats__drv__SingleDiscretePSpace():
    from sympy.stats.drv import SingleDiscretePSpace
    from sympy.stats.drv_types import PoissonDistribution
    assert _test_args(SingleDiscretePSpace(x, PoissonDistribution(1)))

