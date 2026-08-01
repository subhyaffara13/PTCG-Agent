
def test_sympy__stats__crv_types__FDistributionDistribution():
    from sympy.stats.crv_types import FDistributionDistribution
    assert _test_args(FDistributionDistribution(1, 1))

