
def test_sympy__stats__crv_types__GammaDistribution():
    from sympy.stats.crv_types import GammaDistribution
    assert _test_args(GammaDistribution(1, 1))

