
def test_issue_17454():
    x = Symbol('x')
    assert solve((1 - x - I)**4, x) == [1 - I]


def test_issue_17454():
    assert roots([1, -3*(-4 - 4*I)**2/8 + 12*I, 0], multiple=True) == [0, 0]

