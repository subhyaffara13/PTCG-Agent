
def test_sympy__stats__crv_types__LogisticDistribution():
    from sympy.stats.crv_types import LogisticDistribution
    assert _test_args(LogisticDistribution(0, 1))

