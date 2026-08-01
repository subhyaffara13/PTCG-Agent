
def test_issue_13750():
    a = Symbol('a')
    assert limit(erf(a - x), x, oo) == -1
    assert limit(erf(sqrt(x) - x), x, oo) == -1

