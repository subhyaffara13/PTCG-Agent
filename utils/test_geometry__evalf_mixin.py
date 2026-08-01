
def test_geometry_EvalfMixin():
    x = pi
    t = Symbol('t')
    for g in [
            Point(x, x),
            Plane(Point(0, x, 0), (0, 0, x)),
            Curve((x*t, x), (t, 0, x)),
            Ellipse((x, x), x, -x),
            Circle((x, x), x),
            Line((0, x), (x, 0)),
            Segment((0, x), (x, 0)),
            Ray((0, x), (x, 0)),
            Parabola((0, x), Line((-x, 0), (x, 0))),
            Polygon((0, 0), (0, x), (x, 0), (x, x)),
            RegularPolygon((0, x), x, 4, x),
            Triangle((0, 0), (x, 0), (x, x)),
            ]:
        assert str(g).replace('pi', '3.1') == str(g.n(2))

