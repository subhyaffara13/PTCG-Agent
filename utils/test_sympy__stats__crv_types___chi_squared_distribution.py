
def test_sympy__stats__crv_types__ChiSquaredDistribution():
    from sympy.stats.crv_types import ChiSquaredDistribution
    assert _test_args(ChiSquaredDistribution(1))

