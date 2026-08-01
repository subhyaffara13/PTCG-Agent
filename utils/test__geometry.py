
def test_Geometry():
    sT(Point(0, 0), "Point2D(Integer(0), Integer(0))")
    sT(Ellipse(Point(0, 0), 5, 1),
       "Ellipse(Point2D(Integer(0), Integer(0)), Integer(5), Integer(1))")


def test_Geometry():
    assert sstr(Point(0, 0)) == 'Point2D(0, 0)'
    assert sstr(Circle(Point(0, 0), 3)) == 'Circle(Point2D(0, 0), 3)'
    assert sstr(Ellipse(Point(1, 2), 3, 4)) == 'Ellipse(Point2D(1, 2), 3, 4)'
    assert sstr(Triangle(Point(1, 1), Point(7, 8), Point(0, -1))) == \
        'Triangle(Point2D(1, 1), Point2D(7, 8), Point2D(0, -1))'
    assert sstr(Polygon(Point(5, 6), Point(-2, -3), Point(0, 0), Point(4, 7))) == \
        'Polygon(Point2D(5, 6), Point2D(-2, -3), Point2D(0, 0), Point2D(4, 7))'
    assert sstr(Triangle(Point(0, 0), Point(1, 0), Point(0, 1)), sympy_integers=True) == \
        'Triangle(Point2D(S(0), S(0)), Point2D(S(1), S(0)), Point2D(S(0), S(1)))'
    assert sstr(Ellipse(Point(1, 2), 3, 4), sympy_integers=True) == \
        'Ellipse(Point2D(S(1), S(2)), S(3), S(4))'

