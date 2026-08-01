
def test_sympy__stats__drv_types__HermiteDistribution():
    from sympy.stats.drv_types import HermiteDistribution
    assert _test_args(HermiteDistribution(1, 2))

