
def test_sympy__stats__crv_types__VonMisesDistribution():
    from sympy.stats.crv_types import VonMisesDistribution
    assert _test_args(VonMisesDistribution(1, 1))

