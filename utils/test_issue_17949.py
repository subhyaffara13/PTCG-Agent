
def test_issue_17949():
    assert solve(exp(+x+x**2), x) == []
    assert solve(exp(-x+x**2), x) == []
    assert solve(exp(+x-x**2), x) == []
    assert solve(exp(-x-x**2), x) == []

