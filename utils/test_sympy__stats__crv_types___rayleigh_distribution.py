
def test_sympy__stats__crv_types__RayleighDistribution():
    from sympy.stats.crv_types import RayleighDistribution
    assert _test_args(RayleighDistribution(1))

