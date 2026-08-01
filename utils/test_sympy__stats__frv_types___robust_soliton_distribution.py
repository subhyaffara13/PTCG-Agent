
def test_sympy__stats__frv_types__RobustSolitonDistribution():
    from sympy.stats.frv_types import RobustSolitonDistribution
    assert _test_args(RobustSolitonDistribution(1000, 0.5, 0.1))

