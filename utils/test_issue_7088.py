
def test_issue_7088():
    a = Symbol('a')
    assert limit(sqrt(x/(x + a)), x, oo) == 1

