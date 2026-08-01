
def test_sympy__sets__fancysets__ComplexRegion():
    from sympy.sets.fancysets import ComplexRegion
    from sympy.core.singleton import S
    from sympy.sets import Interval
    a = Interval(0, 1)
    b = Interval(2, 3)
    theta = Interval(0, 2*S.Pi)
    assert _test_args(ComplexRegion(a*b))
    assert _test_args(ComplexRegion(a*theta, polar=True))

