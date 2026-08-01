
def test_sympy__stats__crv_types__QuadraticUDistribution():
    from sympy.stats.crv_types import QuadraticUDistribution
    assert _test_args(QuadraticUDistribution(1, 2))

