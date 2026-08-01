
def test_polynomial_relation_simplification():
    assert Ge(3*x*(x + 1) + 4, 3*x).simplify() in [Ge(x**2, -Rational(4,3)), Le(-x**2, Rational(4, 3))]
    assert Le(-(3*x*(x + 1) + 4), -3*x).simplify() in [Ge(x**2, -Rational(4,3)), Le(-x**2, Rational(4, 3))]
    assert ((x**2+3)*(x**2-1)+3*x >= 2*x**2).simplify() in [(x**4 + 3*x >= 3), (-x**4 - 3*x <= -3)]

