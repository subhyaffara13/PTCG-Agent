
def test_sympy__stats__crv_types__GammaInverseDistribution():
    from sympy.stats.crv_types import GammaInverseDistribution
    assert _test_args(GammaInverseDistribution(1, 1))

