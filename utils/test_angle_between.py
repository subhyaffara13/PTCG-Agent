
def test_angle_between():
    a = Point(1, 2, 3, 4)
    b = a.orthogonal_direction
    o = a.origin
    assert feq(Line.angle_between(Line(Point(0, 0), Point(1, 1)),
                                  Line(Point(0, 0), Point(5, 0))).evalf(), pi.evalf() / 4)
    assert Line(a, o).angle_between(Line(b, o)) == pi / 2
    z = Point3D(0, 0, 0)
    assert Line3D.angle_between(Line3D(z, Point3D(1, 1, 1)),
                                Line3D(z, Point3D(5, 0, 0))) == acos(sqrt(3) / 3)
    # direction of points is used to determine angle
    assert Line3D.angle_between(Line3D(z, Point3D(1, 1, 1)),
                                Line3D(Point3D(5, 0, 0), z)) == acos(-sqrt(3) / 3)

