
def test_are_concurrent_3d():
    p1 = Point3D(0, 0, 0)
    l1 = Line(p1, Point3D(1, 1, 1))
    parallel_1 = Line3D(Point3D(0, 0, 0), Point3D(1, 0, 0))
    parallel_2 = Line3D(Point3D(0, 1, 0), Point3D(1, 1, 0))
    assert Line3D.are_concurrent(l1) is False
    assert Line3D.are_concurrent(l1, Line(Point3D(x1, x1, x1), Point3D(y1, y1, y1))) is False
    assert Line3D.are_concurrent(l1, Line3D(p1, Point3D(x1, x1, x1)),
                                 Line(Point3D(x1, x1, x1), Point3D(x1, 1 + x1, 1))) is True
    assert Line3D.are_concurrent(parallel_1, parallel_2) is False

