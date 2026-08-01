
def test_sympy__stats__drv_types__SkellamDistribution():
    from sympy.stats.drv_types import SkellamDistribution
    assert _test_args(SkellamDistribution(1, 1))

