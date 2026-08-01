
def test_issue_11914():
    a, b = Interval(0, 1), Interval(0, pi)
    c, d = Interval(2, 3), Interval(pi, 3 * pi / 2)
    cp1 = ComplexRegion(a * b, polar=True)
    cp2 = ComplexRegion(c * d, polar=True)

    assert -3 in cp1.union(cp2)
    assert -3 in cp2.union(cp1)
    assert -5 not in cp1.union(cp2)

