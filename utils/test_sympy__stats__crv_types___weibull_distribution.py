
def test_sympy__stats__crv_types__WeibullDistribution():
    from sympy.stats.crv_types import WeibullDistribution
    assert _test_args(WeibullDistribution(1, 1))

