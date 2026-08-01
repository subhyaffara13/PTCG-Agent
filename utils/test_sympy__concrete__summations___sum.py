
def test_sympy__concrete__summations__Sum():
    from sympy.concrete.summations import Sum
    assert _test_args(Sum(x, (x, 0, 10)))
    assert _test_args(Sum(x, (x, 0, y), (y, 0, 10)))

