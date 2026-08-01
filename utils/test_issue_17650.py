
def test_issue_17650():
    x = Symbol('x', real=True)
    assert solve(abs(abs(x**2 - 1) - x) - x) == [1, -1 + sqrt(2), 1 + sqrt(2)]

