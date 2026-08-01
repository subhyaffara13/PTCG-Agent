
def test_sympy__stats__crv_types__ReciprocalDistribution():
    from sympy.stats.crv_types import ReciprocalDistribution
    assert _test_args(ReciprocalDistribution(5, 30))

