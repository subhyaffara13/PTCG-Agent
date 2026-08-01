
def test_issue_8755():
    # This tests two things: that if full unrad is attempted and fails
    # the solution should still be found; also it tests the use of
    # keyword `composite`.
    assert len(solve(sqrt(y)*x + x**3 - 1, x)) == 3
    assert len(solve(-512*y**3 + 1344*(x + 2)**Rational(1, 3)*y**2 -
        1176*(x + 2)**Rational(2, 3)*y - 169*x + 686, y, _unrad=False)) == 3

