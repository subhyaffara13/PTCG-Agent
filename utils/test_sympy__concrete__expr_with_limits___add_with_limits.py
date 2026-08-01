
def test_sympy__concrete__expr_with_limits__AddWithLimits():
    from sympy.concrete.expr_with_limits import AddWithLimits
    assert _test_args(AddWithLimits(x, (x, 0, 10)))
    assert _test_args(AddWithLimits(x*y, (x, 0, 10),(y,1,3)))

