
def test_sympy__stats__crv_types__CauchyDistribution():
    from sympy.stats.crv_types import CauchyDistribution
    assert _test_args(CauchyDistribution(0, 1))

