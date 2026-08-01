
def test_sympy__sets__sets__Intersection():
    from sympy.sets.sets import Intersection, Interval
    from sympy.core.symbol import Symbol
    x = Symbol('x')
    y = Symbol('y')
    S = Intersection(Interval(0, x), Interval(y, 1))
    assert isinstance(S, Intersection)
    assert _test_args(S)

