
def test_sympy__stats__crv_types__RaisedCosineDistribution():
    from sympy.stats.crv_types import RaisedCosineDistribution
    assert _test_args(RaisedCosineDistribution(1, 1))

