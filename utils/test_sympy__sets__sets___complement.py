
def test_sympy__sets__sets__Complement():
    from sympy.sets.sets import Complement, Interval
    assert _test_args(Complement(Interval(0, 2), Interval(0, 1)))

