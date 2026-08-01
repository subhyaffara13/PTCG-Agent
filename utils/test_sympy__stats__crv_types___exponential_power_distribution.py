
def test_sympy__stats__crv_types__ExponentialPowerDistribution():
    from sympy.stats.crv_types import ExponentialPowerDistribution
    assert _test_args(ExponentialPowerDistribution(0, 1, 1))

