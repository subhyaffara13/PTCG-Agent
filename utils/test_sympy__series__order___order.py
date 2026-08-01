
def test_sympy__series__order__Order():
    from sympy.series.order import Order
    assert _test_args(Order(1, x, y))

