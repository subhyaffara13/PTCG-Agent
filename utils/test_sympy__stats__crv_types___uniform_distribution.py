
def test_sympy__stats__crv_types__UniformDistribution():
    from sympy.stats.crv_types import UniformDistribution
    assert _test_args(UniformDistribution(0, 1))

