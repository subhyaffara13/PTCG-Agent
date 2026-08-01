
def test_sympy__stats__crv_types__MoyalDistribution():
    from sympy.stats.crv_types import MoyalDistribution
    assert _test_args(MoyalDistribution(1,2))

