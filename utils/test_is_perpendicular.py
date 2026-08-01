
def test_is_perpendicular():
    p1 = Point(0, 0)
    p2 = Point(1, 1)

    l1 = Line(p1, p2)
    l2 = Line(Point(x1, x1), Point(y1, y1))
    l1_1 = Line(p1, Point(-x1, x1))
    # 2D
    assert Line.is_perpendicular(l1, l1_1)
    assert Line.is_perpendicular(l1, l2) is False
    p = l1.random_point()
    assert l1.perpendicular_segment(p) == p
    # 3D
    assert Line3D.is_perpendicular(Line3D(Point3D(0, 0, 0), Point3D(1, 0, 0)),
                                   Line3D(Point3D(0, 0, 0), Point3D(0, 1, 0))) is True
    assert Line3D.is_perpendicular(Line3D(Point3D(0, 0, 0), Point3D(1, 0, 0)),
                                   Line3D(Point3D(0, 1, 0), Point3D(1, 1, 0))) is False
    assert Line3D.is_perpendicular(Line3D(Point3D(0, 0, 0), Point3D(1, 1, 1)),
                                   Line3D(Point3D(x1, x1, x1), Point3D(y1, y1, y1))) is False

