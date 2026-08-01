
def test_multiple_integration():
    assert integrate((x**2)*(y**2), (x, 0, 1), (y, -1, 2)) == Rational(1)
    assert integrate((y**2)*(x**2), x, y) == Rational(1, 9)*(x**3)*(y**3)
    assert integrate(1/(x + 3)/(1 + x)**3, x) == \
        log(3 + x)*Rational(-1, 8) + log(1 + x)*Rational(1, 8) + x/(4 + 8*x + 4*x**2)
    assert integrate(sin(x*y)*y, (x, 0, 1), (y, 0, 1)) == -sin(1) + 1

