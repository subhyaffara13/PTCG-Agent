
def test_nine_point_circle():
    assert Triangle(Point(0, 0), Point(1, 0), Point(0, 1)).nine_point_circle \
        == Circle(Point2D(Rational(1, 4), Rational(1, 4)), sqrt(2)/4)

