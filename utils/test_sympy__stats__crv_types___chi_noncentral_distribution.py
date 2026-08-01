
def test_sympy__stats__crv_types__ChiNoncentralDistribution():
    from sympy.stats.crv_types import ChiNoncentralDistribution
    assert _test_args(ChiNoncentralDistribution(1,1))

