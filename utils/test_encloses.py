
def test_encloses():
    # square with a dimpled left side
    s = Polygon(Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1), \
        Point(S.Half, S.Half))
    # the following is True if the polygon isn't treated as closing on itself
    assert s.encloses(Point(0, S.Half)) is False
    assert s.encloses(Point(S.Half, S.Half)) is False  # it's a vertex
    assert s.encloses(Point(Rational(3, 4), S.Half)) is True

