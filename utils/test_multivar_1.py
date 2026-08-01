
def test_multivar_1():
    assert Order(x + y).expr == x + y
    assert Order(x + 2*y).expr == x + y
    assert (Order(x + y) + x).expr == (x + y)
    assert (Order(x + y) + x**2) == Order(x + y)
    assert (Order(x + y) + 1/x) == 1/x + Order(x + y)
    assert Order(x**2 + y*x).expr == x**2 + y*x

