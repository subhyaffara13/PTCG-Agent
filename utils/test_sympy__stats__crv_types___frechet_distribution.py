
def test_sympy__stats__crv_types__FrechetDistribution():
    from sympy.stats.crv_types import FrechetDistribution
    assert _test_args(FrechetDistribution(1, 1, 1))

