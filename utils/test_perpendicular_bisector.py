
def test_perpendicular_bisector():
    s1 = Segment(Point(0, 0), Point(1, 1))
    aline = Line(Point(S.Half, S.Half), Point(Rational(3, 2), Rational(-1, 2)))
    on_line = Segment(Point(S.Half, S.Half), Point(Rational(3, 2), Rational(-1, 2))).midpoint

    assert s1.perpendicular_bisector().equals(aline)
    assert s1.perpendicular_bisector(on_line).equals(Segment(s1.midpoint, on_line))
    assert s1.perpendicular_bisector(on_line + (1, 0)).equals(aline)

