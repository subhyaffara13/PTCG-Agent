
def test_issue_7982():
    x = Symbol('x')
    # Test that no exception happens
    assert solve([2*x**2 + 5*x + 20 <= 0, x >= 1.5], x) is S.false
    # From #8040
    assert solve([x**3 - 8.08*x**2 - 56.48*x/5 - 106 >= 0, x - 1 <= 0], [x]) is S.false

