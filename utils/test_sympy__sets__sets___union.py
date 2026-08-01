
def test_sympy__sets__sets__Union():
    from sympy.sets.sets import Union, Interval
    assert _test_args(Union(Interval(0, 1), Interval(2, 3)))

