
def test_multivar_mul_1():
    assert Order(x + y)*x == Order(x**2 + y*x, x, y)

