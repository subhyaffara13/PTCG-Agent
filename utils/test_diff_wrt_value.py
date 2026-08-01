
def test_diff_wrt_value():
    assert Expr()._diff_wrt is False
    assert x._diff_wrt is True
    assert f(x)._diff_wrt is True
    assert Derivative(f(x), x)._diff_wrt is True
    assert Derivative(x**2, x)._diff_wrt is False

