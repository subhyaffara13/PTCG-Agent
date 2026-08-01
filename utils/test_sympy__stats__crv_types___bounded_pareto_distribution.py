
def test_sympy__stats__crv_types__BoundedParetoDistribution():
    from sympy.stats.crv_types import BoundedParetoDistribution
    assert _test_args(BoundedParetoDistribution(1, 1, 2))

