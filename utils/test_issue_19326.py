
def test_issue_19326():
    x, y = [i(t) for i in map(Function, 'xy')]
    assert (x*y).subs({x: 1 + x, y: x}) == (1 + x)*x

