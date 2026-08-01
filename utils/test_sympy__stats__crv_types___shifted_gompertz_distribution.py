
def test_sympy__stats__crv_types__ShiftedGompertzDistribution():
    from sympy.stats.crv_types import ShiftedGompertzDistribution
    assert _test_args(ShiftedGompertzDistribution(1, 1))

