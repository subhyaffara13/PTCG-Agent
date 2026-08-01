
def test_sympy__stats__crv_types__LomaxDistribution():
    from sympy.stats.crv_types import LomaxDistribution
    assert _test_args(LomaxDistribution(1, 2))

