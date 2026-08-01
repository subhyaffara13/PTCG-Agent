
def test_parameter_value():
    t = Symbol('t')
    C = Curve([2*t, t**2], (t, 0, 2))
    assert C.parameter_value((2, 1), t) == {t: 1}
    raises(ValueError, lambda: C.parameter_value((2, 0), t))


def test_parameter_value():
    t = Symbol('t')
    e = Ellipse(Point(0, 0), 3, 5)
    assert e.parameter_value((3, 0), t) == {t: 0}
    raises(ValueError, lambda: e.parameter_value((4, 0), t))


def test_parameter_value():
    t = Symbol('t')
    p1, p2 = Point(0, 1), Point(5, 6)
    l = Line(p1, p2)
    assert l.parameter_value((5, 6), t) == {t: 1}
    raises(ValueError, lambda: l.parameter_value((0, 0), t))


def test_parameter_value():
    t, u, v = symbols("t, u v")
    p1, p2, p3 = Point(0, 0, 0), Point(0, 0, 1), Point(0, 1, 0)
    p = Plane(p1, p2, p3)
    assert p.parameter_value((0, -3, 2), t) == {t: asin(2*sqrt(13)/13)}
    assert p.parameter_value((0, -3, 2), u, v) == {u: 3, v: 2}
    assert p.parameter_value(p1, t) == p1
    raises(ValueError, lambda: p.parameter_value((1, 0, 0), t))
    raises(ValueError, lambda: p.parameter_value(Line(Point(0, 0), Point(1, 1)), t))
    raises(ValueError, lambda: p.parameter_value((0, -3, 2), t, 1))


def test_parameter_value():
    t = Symbol('t')
    sq = Polygon((0, 0), (0, 1), (1, 1), (1, 0))
    assert sq.parameter_value((0.5, 1), t) == {t: Rational(3, 8)}
    q = Polygon((0, 0), (2, 1), (2, 4), (4, 0))
    assert q.parameter_value((4, 0), t) == {t: -6 + 3*sqrt(5)} # ~= 0.708

    raises(ValueError, lambda: sq.parameter_value((5, 6), t))
    raises(ValueError, lambda: sq.parameter_value(Circle(Point(0, 0), 1), t))

