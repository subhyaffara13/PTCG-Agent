
def test_sympy__stats__drv_types__DiscreteDistributionHandmade():
    from sympy.stats.drv_types import DiscreteDistributionHandmade
    from sympy.core.function import Lambda
    from sympy.sets.sets import FiniteSet
    from sympy.abc import x
    assert _test_args(DiscreteDistributionHandmade(Lambda(x, Rational(1, 10)),
                                                    FiniteSet(*range(10))))

