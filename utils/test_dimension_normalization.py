
def test_dimension_normalization():
    with warns(UserWarning, test_stacklevel=False):
        assert Ray((1, 1), (2, 1, 2)) == Ray((1, 1, 0), (2, 1, 2))


def test_dimension_normalization():
    A = Plane(Point3D(1, 1, 2), normal_vector=(1, 1, 1))
    b = Point(1, 1)
    assert A.projection(b) == Point(Rational(5, 3), Rational(5, 3), Rational(2, 3))

    a, b = Point(0, 0), Point3D(0, 1)
    Z = (0, 0, 1)
    p = Plane(a, normal_vector=Z)
    assert p.perpendicular_plane(a, b) == Plane(Point3D(0, 0, 0), (1, 0, 0))
    assert Plane((1, 2, 1), (2, 1, 0), (3, 1, 2)
        ).intersection((2, 1)) == [Point(2, 1, 0)]

