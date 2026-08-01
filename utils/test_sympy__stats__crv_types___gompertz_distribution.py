
def test_sympy__stats__crv_types__GompertzDistribution():
    from sympy.stats.crv_types import GompertzDistribution
    assert _test_args(GompertzDistribution(1, 1))

