
def test_issue_8615():
    a = Line3D(Point3D(6, 5, 0), Point3D(6, -6, 0))
    b = Line3D(Point3D(6, -1, 19/10), Point3D(6, -1, 0))
    assert a.intersection(b) == [Point3D(6, -1, 0)]

