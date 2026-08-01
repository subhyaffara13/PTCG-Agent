
def test_sympy__sets__fancysets__PolarComplexRegion():
    from sympy.sets.fancysets import PolarComplexRegion
    from sympy.core.singleton import S
    from sympy.sets import Interval
    a = Interval(0, 1)
    theta = Interval(0, 2*S.Pi)
    assert _test_args(PolarComplexRegion(a*theta))

