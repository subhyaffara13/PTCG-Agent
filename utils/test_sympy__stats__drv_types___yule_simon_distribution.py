
def test_sympy__stats__drv_types__YuleSimonDistribution():
    from sympy.stats.drv_types import YuleSimonDistribution
    assert _test_args(YuleSimonDistribution(.5))

