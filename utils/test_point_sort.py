
def test_point_sort():
    assert point_sort([Point(0, 0), Point(1, 0), Point(1, 1)]) == \
        [Point2D(1, 1), Point2D(1, 0), Point2D(0, 0)]

    fig6 = Polygon((0, 0), (1, 0), (1, 1))
    assert polytope_integrate(fig6, x*y) == Rational(-1, 8)
    assert polytope_integrate(fig6, x*y, clockwise = True) == Rational(1, 8)

