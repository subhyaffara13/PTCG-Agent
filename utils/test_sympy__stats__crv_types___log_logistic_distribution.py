
def test_sympy__stats__crv_types__LogLogisticDistribution():
    from sympy.stats.crv_types import LogLogisticDistribution
    assert _test_args(LogLogisticDistribution(1, 1))

