
def test_sympy__stats__crv_types__LogCauchyDistribution():
    from sympy.stats.crv_types import LogCauchyDistribution
    assert _test_args(LogCauchyDistribution(0, 1))

