
def test_sympy__stats__crv_types__LevyDistribution():
    from sympy.stats.crv_types import LevyDistribution
    assert _test_args(LevyDistribution(0, 1))

