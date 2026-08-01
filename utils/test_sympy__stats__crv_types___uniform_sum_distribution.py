
def test_sympy__stats__crv_types__UniformSumDistribution():
    from sympy.stats.crv_types import UniformSumDistribution
    assert _test_args(UniformSumDistribution(1))

