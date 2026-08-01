
def test_sympy__sets__setexpr__SetExpr():
    from sympy.sets.setexpr import SetExpr
    from sympy.sets.sets import Interval
    assert _test_args(SetExpr(Interval(0, 1)))

