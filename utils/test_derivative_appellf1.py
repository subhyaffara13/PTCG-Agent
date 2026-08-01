
def test_derivative_appellf1():
    from sympy.core.function import diff
    a, b1, b2, c, x, y, z = symbols('a b1 b2 c x y z')
    assert diff(appellf1(a, b1, b2, c, x, y), x) == a*b1*appellf1(a + 1, b2, b1 + 1, c + 1, y, x)/c
    assert diff(appellf1(a, b1, b2, c, x, y), y) == a*b2*appellf1(a + 1, b1, b2 + 1, c + 1, x, y)/c
    assert diff(appellf1(a, b1, b2, c, x, y), z) == 0
    assert diff(appellf1(a, b1, b2, c, x, y), a) ==  Derivative(appellf1(a, b1, b2, c, x, y), a)

