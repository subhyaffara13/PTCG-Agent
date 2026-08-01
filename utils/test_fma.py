
def test_fma():
    x, y, z = symbols('x y z')

    # Expand
    assert fma(x, y, z).expand(func=True) - x*y - z == 0

    expr = fma(17*x, 42*y, 101*z)

    # Diff
    assert expr.diff(x) - expr.expand(func=True).diff(x) == 0
    assert expr.diff(y) - expr.expand(func=True).diff(y) == 0
    assert expr.diff(z) - expr.expand(func=True).diff(z) == 0

    assert expr.diff(x) - 17*42*y == 0
    assert expr.diff(y) - 17*42*x == 0
    assert expr.diff(z) - 101 == 0

