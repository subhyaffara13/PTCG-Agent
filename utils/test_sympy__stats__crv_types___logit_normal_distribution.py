
def test_sympy__stats__crv_types__LogitNormalDistribution():
    from sympy.stats.crv_types import LogitNormalDistribution
    assert _test_args(LogitNormalDistribution(0, 1))

