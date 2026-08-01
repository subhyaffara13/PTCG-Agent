
def test_multiple_derivative():
    # Issue #15007
    assert f(x, y).diff(y, y, x, y, x
        ) == Derivative(f(x, y), (x, 2), (y, 3))

