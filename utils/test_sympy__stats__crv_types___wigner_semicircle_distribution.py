
def test_sympy__stats__crv_types__WignerSemicircleDistribution():
    from sympy.stats.crv_types import WignerSemicircleDistribution
    assert _test_args(WignerSemicircleDistribution(1))

