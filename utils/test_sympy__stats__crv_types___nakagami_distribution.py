
def test_sympy__stats__crv_types__NakagamiDistribution():
    from sympy.stats.crv_types import NakagamiDistribution
    assert _test_args(NakagamiDistribution(1, 1))

