
def test_sympy__stats__drv_types__ZetaDistribution():
    from sympy.stats.drv_types import ZetaDistribution
    assert _test_args(ZetaDistribution(1.5))

