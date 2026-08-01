
def test_sympy__stats__crv_types__TriangularDistribution():
    from sympy.stats.crv_types import TriangularDistribution
    assert _test_args(TriangularDistribution(-1, 0, 1))

