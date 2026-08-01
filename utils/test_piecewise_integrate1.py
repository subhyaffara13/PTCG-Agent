
def test_piecewise_integrate1():
    x, y = symbols('x y', real=True)

    f = Piecewise(((x - 2)**2, x >= 0), (1, True))
    assert integrate(f, (x, -2, 2)) == Rational(14, 3)

    g = Piecewise(((x - 5)**5, x >= 4), (f, True))
    assert integrate(g, (x, -2, 2)) == Rational(14, 3)
    assert integrate(g, (x, -2, 5)) == Rational(43, 6)

    assert g == Piecewise(((x - 5)**5, x >= 4), (f, x < 4))

    g = Piecewise(((x - 5)**5, 2 <= x), (f, x < 2))
    assert integrate(g, (x, -2, 2)) == Rational(14, 3)
    assert integrate(g, (x, -2, 5)) == Rational(-701, 6)

    assert g == Piecewise(((x - 5)**5, 2 <= x), (f, True))

    g = Piecewise(((x - 5)**5, 2 <= x), (2*f, True))
    assert integrate(g, (x, -2, 2)) == Rational(28, 3)
    assert integrate(g, (x, -2, 5)) == Rational(-673, 6)

