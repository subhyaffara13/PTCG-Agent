
def test_issue_24650():
    x = symbols('x')
    r = solve(Eq(Piecewise((x, Eq(x, 0) | (x > 1))), 0))
    assert r == [0]
    r = checksol(Eq(Piecewise((x, Eq(x, 0) | (x > 1))), 0), x, sol=0)
    assert r is True

