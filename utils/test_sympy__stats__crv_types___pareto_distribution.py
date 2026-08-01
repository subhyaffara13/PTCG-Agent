
def test_sympy__stats__crv_types__ParetoDistribution():
    from sympy.stats.crv_types import ParetoDistribution
    assert _test_args(ParetoDistribution(1, 1))

