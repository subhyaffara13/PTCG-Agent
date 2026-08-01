
def test_contains_nonreal_symbols():
    u, v, w, z = symbols('u, v, w, z')
    l = Segment(Point(u, w), Point(v, z))
    p = Point(u*Rational(2, 3) + v/3, w*Rational(2, 3) + z/3)
    assert l.contains(p)

