
def test_sympy__stats__crv_types__BetaNoncentralDistribution():
    from sympy.stats.crv_types import BetaNoncentralDistribution
    assert _test_args(BetaNoncentralDistribution(1, 1, 1))

