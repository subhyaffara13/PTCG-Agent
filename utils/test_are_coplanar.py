
def test_are_coplanar():
    a = Line3D(Point3D(5, 0, 0), Point3D(1, -1, 1))
    b = Line3D(Point3D(0, -2, 0), Point3D(3, 1, 1))
    c = Line3D(Point3D(0, -1, 0), Point3D(5, -1, 9))
    d = Line(Point2D(0, 3), Point2D(1, 5))

    assert are_coplanar(a, b, c) == False
    assert are_coplanar(a, d) == False

