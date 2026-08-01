
def test_issue_7228():
    assert solve(4**(2*(x**2) + 2*x) - 8, x) == [Rational(-3, 2), S.Half]

