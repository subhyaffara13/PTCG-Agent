
def test_sympy__sets__fancysets__CartesianComplexRegion():
    from sympy.sets.fancysets import CartesianComplexRegion
    from sympy.sets import Interval
    a = Interval(0, 1)
    b = Interval(2, 3)
    assert _test_args(CartesianComplexRegion(a*b))

