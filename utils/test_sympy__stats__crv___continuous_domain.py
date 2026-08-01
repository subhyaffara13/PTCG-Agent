
def test_sympy__stats__crv__ContinuousDomain():
    from sympy.sets.sets import Interval
    from sympy.stats.crv import ContinuousDomain
    assert _test_args(ContinuousDomain({x}, Interval(-oo, oo)))

