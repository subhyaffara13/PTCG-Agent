
def test_sympy__stats__crv_types__NormalDistribution():
    from sympy.stats.crv_types import NormalDistribution
    assert _test_args(NormalDistribution(0, 1))

