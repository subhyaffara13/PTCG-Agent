
def test_sympy__concrete__expr_with_limits__ExprWithLimits():
    from sympy.concrete.expr_with_limits import ExprWithLimits
    assert _test_args(ExprWithLimits(x, (x, 0, 10)))
    assert _test_args(ExprWithLimits(x*y, (x, 0, 10.),(y,1.,3)))

