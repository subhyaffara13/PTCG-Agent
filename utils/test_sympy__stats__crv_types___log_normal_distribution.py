
def test_sympy__stats__crv_types__LogNormalDistribution():
    from sympy.stats.crv_types import LogNormalDistribution
    assert _test_args(LogNormalDistribution(0, 1))

