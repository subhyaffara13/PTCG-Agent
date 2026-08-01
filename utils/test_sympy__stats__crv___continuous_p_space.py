
def test_sympy__stats__crv__ContinuousPSpace():
    from sympy.sets.sets import Interval
    from sympy.stats.crv import ContinuousPSpace, SingleContinuousDomain
    D = SingleContinuousDomain(x, Interval(-oo, oo))
    assert _test_args(ContinuousPSpace(D, nd))

