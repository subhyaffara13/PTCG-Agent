
def test_length():
    assert length(2, 1, 0) == 1
    assert length(-2, 4, 5) == 3
    assert length(-5, 4, 17) == 4
    assert length(0, 4, 13) == 6
    assert length(7, 13, 11) == 23
    assert length(1, 6, 4) == 2


def test_length():
    t = Symbol('t', real=True)

    c1 = Curve((t, 0), (t, 0, 1))
    assert c1.length == 1

    c2 = Curve((t, t), (t, 0, 1))
    assert c2.length == sqrt(2)

    c3 = Curve((t ** 2, t), (t, 2, 5))
    assert c3.length == -sqrt(17) - asinh(4) / 4 + asinh(10) / 4 + 5 * sqrt(101) / 2


def test_length():
    s2 = Segment3D(Point3D(x1, x1, x1), Point3D(y1, y1, y1))
    assert Line(Point(0, 0), Point(1, 1)).length is oo
    assert s2.length == sqrt(3) * sqrt((x1 - y1) ** 2)
    assert Line3D(Point3D(0, 0, 0), Point3D(1, 1, 1)).length is oo


def test_length():
    return 20

