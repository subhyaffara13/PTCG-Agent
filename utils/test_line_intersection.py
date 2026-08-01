
def test_line_intersection():
    # see also test_issue_11238 in test_matrices.py
    x0 = tan(pi*Rational(13, 45))
    x1 = sqrt(3)
    x2 = x0**2
    x, y = [8*x0/(x0 + x1), (24*x0 - 8*x1*x2)/(x2 - 3)]
    assert Line(Point(0, 0), Point(1, -sqrt(3))).contains(Point(x, y)) is True

