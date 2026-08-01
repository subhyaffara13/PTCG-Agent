
def test_object_from_equation():
    from sympy.abc import x, y, a, b, c, d, e
    assert Circle(x**2 + y**2 + 3*x + 4*y - 8) == Circle(Point2D(S(-3) / 2, -2), sqrt(57) / 2)
    assert Circle(x**2 + y**2 + 6*x + 8*y + 25) == Circle(Point2D(-3, -4), 0)
    assert Circle(a**2 + b**2 + 6*a + 8*b + 25, x='a', y='b') == Circle(Point2D(-3, -4), 0)
    assert Circle(x**2 + y**2 - 25) == Circle(Point2D(0, 0), 5)
    assert Circle(x**2 + y**2) == Circle(Point2D(0, 0), 0)
    assert Circle(a**2 + b**2, x='a', y='b') == Circle(Point2D(0, 0), 0)
    assert Circle(x**2 + y**2 + 6*x + 8) == Circle(Point2D(-3, 0), 1)
    assert Circle(x**2 + y**2 + 6*y + 8) == Circle(Point2D(0, -3), 1)
    assert Circle((x - 1)**2 + y**2 - 9) == Circle(Point2D(1, 0), 3)
    assert Circle(6*(x**2) + 6*(y**2) + 6*x + 8*y - 25) == Circle(Point2D(Rational(-1, 2), Rational(-2, 3)), 5*sqrt(7)/6)
    assert Circle(Eq(a**2 + b**2, 25), x='a', y=b) == Circle(Point2D(0, 0), 5)
    raises(GeometryError, lambda: Circle(x**2 + y**2 + 3*x + 4*y + 26))
    raises(GeometryError, lambda: Circle(x**2 + y**2 + 25))
    raises(GeometryError, lambda: Circle(a**2 + b**2 + 25, x='a', y='b'))
    raises(GeometryError, lambda: Circle(x**2 + 6*y + 8))
    raises(GeometryError, lambda: Circle(6*(x ** 2) + 4*(y**2) + 6*x + 8*y + 25))
    raises(ValueError, lambda: Circle(a**2 + b**2 + 3*a + 4*b - 8))
    # .equation() adds 'real=True' assumption; '==' would fail if assumptions differed
    x, y = symbols('x y', real=True)
    eq = a*x**2 + a*y**2 + c*x + d*y + e
    assert expand(Circle(eq).equation()*a) == eq


def test_object_from_equation():
    from sympy.abc import x, y, a, b
    assert Line(3*x + y + 18) == Line2D(Point2D(0, -18), Point2D(1, -21))
    assert Line(3*x + 5 * y + 1) == Line2D(
        Point2D(0, Rational(-1, 5)), Point2D(1, Rational(-4, 5)))
    assert Line(3*a + b + 18, x="a", y="b") == Line2D(
        Point2D(0, -18), Point2D(1, -21))
    assert Line(3*x + y) == Line2D(Point2D(0, 0), Point2D(1, -3))
    assert Line(x + y) == Line2D(Point2D(0, 0), Point2D(1, -1))
    assert Line(Eq(3*a + b, -18), x="a", y=b) == Line2D(
        Point2D(0, -18), Point2D(1, -21))
    # issue 22361
    assert Line(x - 1) == Line2D(Point2D(1, 0), Point2D(1, 1))
    assert Line(2*x - 2, y=x) == Line2D(Point2D(0, 1), Point2D(1, 1))
    assert Line(y) == Line2D(Point2D(0, 0), Point2D(1, 0))
    assert Line(2*y, x=y) == Line2D(Point2D(0, 0), Point2D(0, 1))
    assert Line(y, x=y) == Line2D(Point2D(0, 0), Point2D(0, 1))
    raises(ValueError, lambda: Line(x / y))
    raises(ValueError, lambda: Line(a / b, x='a', y='b'))
    raises(ValueError, lambda: Line(y / x))
    raises(ValueError, lambda: Line(b / a, x='a', y='b'))
    raises(ValueError, lambda: Line((x + 1)**2 + y))

