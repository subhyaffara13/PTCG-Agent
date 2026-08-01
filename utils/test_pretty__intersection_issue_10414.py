
def test_pretty_Intersection_issue_10414():
    x, y, z, w = symbols('x, y, z, w')
    a, b = Interval(x, y), Interval(z, w)
    ucode_str = '[x, y] ∩ [z, w]'
    ascii_str = '[x, y] n [z, w]'
    assert upretty(Intersection(a, b)) == ucode_str
    assert pretty(Intersection(a, b)) == ascii_str

