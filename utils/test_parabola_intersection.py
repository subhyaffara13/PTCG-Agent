
def test_parabola_intersection():
    l1 = Line(Point(1, -2), Point(-1,-2))
    l2 = Line(Point(1, 2), Point(-1,2))
    l3 = Line(Point(1, 0), Point(-1,0))

    p1 = Point(0,0)
    p2 = Point(0, -2)
    p3 = Point(120, -12)
    parabola1 = Parabola(p1, l1)

    # parabola with parabola
    assert parabola1.intersection(parabola1) == [parabola1]
    assert parabola1.intersection(Parabola(p1, l2)) == [Point2D(-2, 0), Point2D(2, 0)]
    assert parabola1.intersection(Parabola(p2, l3)) == [Point2D(0, -1)]
    assert parabola1.intersection(Parabola(Point(16, 0), l1)) == [Point2D(8, 15)]
    assert parabola1.intersection(Parabola(Point(0, 16), l1)) == [Point2D(-6, 8), Point2D(6, 8)]
    assert parabola1.intersection(Parabola(p3, l3)) == []
    # parabola with point
    assert parabola1.intersection(p1) == []
    assert parabola1.intersection(Point2D(0, -1)) == [Point2D(0, -1)]
    assert parabola1.intersection(Point2D(4, 3)) == [Point2D(4, 3)]
    # parabola with line
    assert parabola1.intersection(Line(Point2D(-7, 3), Point(12, 3))) == [Point2D(-4, 3), Point2D(4, 3)]
    assert parabola1.intersection(Line(Point(-4, -1), Point(4, -1))) == [Point(0, -1)]
    assert parabola1.intersection(Line(Point(2, 0), Point(0, -2))) == [Point2D(2, 0)]
    raises(TypeError, lambda: parabola1.intersection(Line(Point(0, 0, 0), Point(1, 1, 1))))
    # parabola with segment
    assert parabola1.intersection(Segment2D((-4, -5), (4, 3))) == [Point2D(0, -1), Point2D(4, 3)]
    assert parabola1.intersection(Segment2D((0, -5), (0, 6))) == [Point2D(0, -1)]
    assert parabola1.intersection(Segment2D((-12, -65), (14, -68))) == []
    # parabola with ray
    assert parabola1.intersection(Ray2D((-4, -5), (4, 3))) == [Point2D(0, -1), Point2D(4, 3)]
    assert parabola1.intersection(Ray2D((0, 7), (1, 14))) == [Point2D(14 + 2*sqrt(57), 105 + 14*sqrt(57))]
    assert parabola1.intersection(Ray2D((0, 7), (0, 14))) == []
    # parabola with ellipse/circle
    assert parabola1.intersection(Circle(p1, 2)) == [Point2D(-2, 0), Point2D(2, 0)]
    assert parabola1.intersection(Circle(p2, 1)) == [Point2D(0, -1)]
    assert parabola1.intersection(Ellipse(p2, 2, 1)) == [Point2D(0, -1)]
    assert parabola1.intersection(Ellipse(Point(0, 19), 5, 7)) == []
    assert parabola1.intersection(Ellipse((0, 3), 12, 4)) == [
           Point2D(0, -1),
           Point2D(-4*sqrt(17)/3, Rational(59, 9)),
           Point2D(4*sqrt(17)/3, Rational(59, 9))]
    # parabola with unsupported type
    raises(TypeError, lambda: parabola1.intersection(2))

