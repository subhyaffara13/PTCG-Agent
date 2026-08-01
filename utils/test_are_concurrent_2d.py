
def test_are_concurrent_2d():
    l1 = Line(Point(0, 0), Point(1, 1))
    l2 = Line(Point(x1, x1), Point(x1, 1 + x1))
    assert Line.are_concurrent(l1) is False
    assert Line.are_concurrent(l1, l2)
    assert Line.are_concurrent(l1, l1, l1, l2)
    assert Line.are_concurrent(l1, l2, Line(Point(5, x1), Point(Rational(-3, 5), x1)))
    assert Line.are_concurrent(l1, Line(Point(0, 0), Point(-x1, x1)), l2) is False

