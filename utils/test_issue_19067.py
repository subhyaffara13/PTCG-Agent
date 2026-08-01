
def test_issue_19067():
    x = Symbol('x')
    assert limit(gamma(x)/(gamma(x - 1)*gamma(x + 2)), x, 0) == -1

