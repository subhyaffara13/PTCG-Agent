
def test_issue_21785():
    a = Symbol('a')
    assert sqrt((-a**2 + x**2)/(1 - x**2)).limit(a, 1, '-') == I

