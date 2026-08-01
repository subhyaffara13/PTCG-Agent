
def test_sympy__stats__crv_types__BeniniDistribution():
    from sympy.stats.crv_types import BeniniDistribution
    assert _test_args(BeniniDistribution(1, 1, 1))

