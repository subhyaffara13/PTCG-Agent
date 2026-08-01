
def test_sympy__stats__crv_types__FisherZDistribution():
    from sympy.stats.crv_types import FisherZDistribution
    assert _test_args(FisherZDistribution(1, 1))

