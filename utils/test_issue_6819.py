
def test_issue_6819():
    a, b, c, d = symbols('a b c d', positive=True)
    assert solve(a*b**x - c*d**x, x) == [log(c/a)/log(b/d)]

