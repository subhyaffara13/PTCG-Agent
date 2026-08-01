
def test_issue_6843():
    n = Symbol('n', integer=True, positive=True)
    r = (n + 1)*x**(n + 1)/(x**(n + 1) - 1) - x/(x - 1)
    assert gruntz(r, x, 1).simplify() == n/2

