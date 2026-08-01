
def test_sympy__stats__drv_types__GeometricDistribution():
    from sympy.stats.drv_types import GeometricDistribution
    assert _test_args(GeometricDistribution(.5))

