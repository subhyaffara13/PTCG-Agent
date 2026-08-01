
def test_order_oo():
    x = Symbol('x', positive=True)
    assert Order(x)*oo != Order(1, x)
    assert limit(oo/(x**2 - 4), x, oo) is oo

