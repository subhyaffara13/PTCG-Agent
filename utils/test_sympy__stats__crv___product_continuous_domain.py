
def test_sympy__stats__crv__ProductContinuousDomain():
    from sympy.sets.sets import Interval
    from sympy.stats.crv import SingleContinuousDomain, ProductContinuousDomain
    D = SingleContinuousDomain(x, Interval(-oo, oo))
    E = SingleContinuousDomain(y, Interval(0, oo))
    assert _test_args(ProductContinuousDomain(D, E))

