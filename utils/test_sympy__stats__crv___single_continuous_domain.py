
def test_sympy__stats__crv__SingleContinuousDomain():
    from sympy.sets.sets import Interval
    from sympy.stats.crv import SingleContinuousDomain
    assert _test_args(SingleContinuousDomain(x, Interval(-oo, oo)))

