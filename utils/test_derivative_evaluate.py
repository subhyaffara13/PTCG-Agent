
def test_derivative_evaluate():
    assert Derivative(sin(x), x) != diff(sin(x), x)
    assert Derivative(sin(x), x).doit() == diff(sin(x), x)

    assert Derivative(Derivative(f(x), x), x) == diff(f(x), x, x)
    assert Derivative(sin(x), x, 0) == sin(x)
    assert Derivative(sin(x), (x, y), (x, -y)) == sin(x)

