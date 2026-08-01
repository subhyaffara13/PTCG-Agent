
def test_order_symbols():
    e = x*y*sin(x)*Integral(x, (x, 1, 2))
    assert O(e) == O(x**2*y, x, y)
    assert O(e, x) == O(x**2)

