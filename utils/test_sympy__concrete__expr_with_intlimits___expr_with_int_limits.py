
def test_sympy__concrete__expr_with_intlimits__ExprWithIntLimits():
    from sympy.concrete.expr_with_intlimits import ExprWithIntLimits
    assert _test_args(ExprWithIntLimits(x, (x, 0, 10)))
    assert _test_args(ExprWithIntLimits(x*y, (x, 0, 10),(y,1,3)))

