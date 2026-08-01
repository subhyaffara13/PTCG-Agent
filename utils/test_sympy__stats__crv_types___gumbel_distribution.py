
def test_sympy__stats__crv_types__GumbelDistribution():
    from sympy.stats.crv_types import GumbelDistribution
    assert _test_args(GumbelDistribution(1, 1, False))

