
def test_sympy__stats__drv_types__FlorySchulzDistribution():
    from sympy.stats.drv_types import FlorySchulzDistribution
    assert _test_args(FlorySchulzDistribution(.5))

