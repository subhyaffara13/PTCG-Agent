
def test_raises():
    assert raises(ZeroDivisionError, lambda: 1 / 0)
    assert not raises(ZeroDivisionError, lambda: 1)


def test_raises():
    d, e = symbols('a,b', real=True)
    s = Segment((d, 0), (e, 0))

    raises(TypeError, lambda: Line((1, 1), 1))
    raises(ValueError, lambda: Line(Point(0, 0), Point(0, 0)))
    raises(Undecidable, lambda: Point(2 * d, 0) in s)
    raises(ValueError, lambda: Ray3D(Point(1.0, 1.0)))
    raises(ValueError, lambda: Line3D(Point3D(0, 0, 0), Point3D(0, 0, 0)))
    raises(TypeError, lambda: Line3D((1, 1), 1))
    raises(ValueError, lambda: Line3D(Point3D(0, 0, 0)))
    raises(TypeError, lambda: Ray((1, 1), 1))
    raises(GeometryError, lambda: Line(Point(0, 0), Point(1, 0))
           .projection(Circle(Point(0, 0), 1)))


def test_raises():
    # input validation
    with pytest.raises(ValueError, match=r"d must be a non-negative integer"):
        RandomEngine((2,))

    with pytest.raises(ValueError, match=r"d must be a non-negative integer"):
        RandomEngine(-1)

    msg = r"'u_bounds' and 'l_bounds' must be integers"
    with pytest.raises(ValueError, match=msg):
        engine = RandomEngine(1)
        engine.integers(l_bounds=1, u_bounds=1.1)


def test_raises():
    for ver in ['1.9', '1,9.0', '1.7.x']:
        assert_raises(ValueError, NumpyVersion, ver)

