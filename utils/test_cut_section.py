
def test_cut_section():
    # concave polygon
    p = Polygon((-1, -1), (1, Rational(5, 2)), (2, 1), (3, Rational(5, 2)), (4, 2), (5, 3), (-1, 3))
    l = Line((0, 0), (Rational(9, 2), 3))
    p1 = p.cut_section(l)[0]
    p2 = p.cut_section(l)[1]
    assert p1 == Polygon(
        Point2D(Rational(-9, 13), Rational(-6, 13)), Point2D(1, Rational(5, 2)), Point2D(Rational(24, 13), Rational(16, 13)),
        Point2D(Rational(12, 5), Rational(8, 5)), Point2D(3, Rational(5, 2)), Point2D(Rational(24, 7), Rational(16, 7)),
        Point2D(Rational(9, 2), 3), Point2D(-1, 3), Point2D(-1, Rational(-2, 3)))
    assert p2 == Polygon(Point2D(-1, -1), Point2D(Rational(-9, 13), Rational(-6, 13)), Point2D(Rational(24, 13), Rational(16, 13)),
        Point2D(2, 1), Point2D(Rational(12, 5), Rational(8, 5)), Point2D(Rational(24, 7), Rational(16, 7)), Point2D(4, 2), Point2D(5, 3),
        Point2D(Rational(9, 2), 3), Point2D(-1, Rational(-2, 3)))

    # convex polygon
    p = RegularPolygon(Point2D(0, 0), 6, 6)
    s = p.cut_section(Line((0, 0), slope=1))
    assert s[0] == Polygon(Point2D(-3*sqrt(3) + 9, -3*sqrt(3) + 9), Point2D(3, 3*sqrt(3)),
        Point2D(-3, 3*sqrt(3)), Point2D(-6, 0), Point2D(-9 + 3*sqrt(3), -9 + 3*sqrt(3)))
    assert s[1] == Polygon(Point2D(6, 0), Point2D(-3*sqrt(3) + 9, -3*sqrt(3) + 9),
        Point2D(-9 + 3*sqrt(3), -9 + 3*sqrt(3)), Point2D(-3, -3*sqrt(3)), Point2D(3, -3*sqrt(3)))

    # case where line does not intersects but coincides with the edge of polygon
    a, b = 20, 10
    t1, t2, t3, t4 = [(0, b), (0, 0), (a, 0), (a, b)]
    p = Polygon(t1, t2, t3, t4)
    p1, p2 = p.cut_section(Line((0, b), slope=0))
    assert p1 == None
    assert p2 == Polygon(Point2D(0, 10), Point2D(0, 0), Point2D(20, 0), Point2D(20, 10))

    p3, p4 = p.cut_section(Line((0, 0), slope=0))
    assert p3 == Polygon(Point2D(0, 10), Point2D(0, 0), Point2D(20, 0), Point2D(20, 10))
    assert p4 == None

    # case where the line does not intersect with a polygon at all
    raises(ValueError, lambda: p.cut_section(Line((0, a), slope=0)))

