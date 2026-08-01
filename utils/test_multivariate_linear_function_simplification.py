
def test_multivariate_linear_function_simplification():
    assert Ge(x + y, x - y).simplify() == Ge(y, 0)
    assert Le(-x + y, -x - y).simplify() == Le(y, 0)
    assert Eq(2*x + y, 2*x + y - 3).simplify() == False
    assert (2*x + y > 2*x + y - 3).simplify() == True
    assert (2*x + y < 2*x + y - 3).simplify() == False
    assert (2*x + y < 2*x + y + 3).simplify() == True
    a, b, c, d, e, f, g = symbols('a b c d e f g')
    assert Lt(a + b + c + 2*d, 3*d - f + g). simplify() == Lt(a, -b - c + d - f + g)

