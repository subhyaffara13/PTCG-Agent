
def test_issue_11617():
    p1 = Point3D(1,0,2)
    p2 = Point2D(2,0)

    with warns(UserWarning, test_stacklevel=False):
        assert p1.distance(p2) == sqrt(5)

