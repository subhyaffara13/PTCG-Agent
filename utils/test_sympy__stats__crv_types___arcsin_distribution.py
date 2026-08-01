
def test_sympy__stats__crv_types__ArcsinDistribution():
    from sympy.stats.crv_types import ArcsinDistribution
    assert _test_args(ArcsinDistribution(0, 1))

