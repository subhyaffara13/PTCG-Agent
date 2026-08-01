
def test_sympy__stats__crv_types__ContinuousDistributionHandmade():
    from sympy.stats.crv_types import ContinuousDistributionHandmade
    from sympy.core.function import Lambda
    from sympy.sets.sets import Interval
    from sympy.abc import x
    assert _test_args(ContinuousDistributionHandmade(Lambda(x, 2*x),
                                                     Interval(0, 1)))

