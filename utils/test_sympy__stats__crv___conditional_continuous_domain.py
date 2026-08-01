
def test_sympy__stats__crv__ConditionalContinuousDomain():
    from sympy.sets.sets import Interval
    from sympy.stats.crv import (SingleContinuousDomain,
            ConditionalContinuousDomain)
    D = SingleContinuousDomain(x, Interval(-oo, oo))
    assert _test_args(ConditionalContinuousDomain(D, x > 0))

