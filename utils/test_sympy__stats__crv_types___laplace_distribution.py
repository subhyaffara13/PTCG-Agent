
def test_sympy__stats__crv_types__LaplaceDistribution():
    from sympy.stats.crv_types import LaplaceDistribution
    assert _test_args(LaplaceDistribution(0, 1))

