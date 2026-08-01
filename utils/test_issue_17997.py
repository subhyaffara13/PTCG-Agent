
def test_issue_17997():
    t, s = symbols('t s')
    c = Curve((t, t**2), (t, 0, 10))
    p = Curve([2*s, s**2], (s, 0, 2))
    assert c(2) == Point(2, 4)
    assert p(1) == Point(2, 1)

