
def test_issue_21004():
    x = symbols('x')
    f = x/sqrt(x**2+1)
    f_diff = f.diff(x)
    assert solve(f_diff, x) == []

