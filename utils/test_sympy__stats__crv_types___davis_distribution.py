
def test_sympy__stats__crv_types__DavisDistribution():
    from sympy.stats.crv_types import DavisDistribution
    assert _test_args(DavisDistribution(1, 1, 1))

