
def test_issue_3539():
    a = Wild('a')
    x = Symbol('x')
    assert (x - 2).match(a - x) is None
    assert (6/x).match(a*x) is None
    assert (6/x**2).match(a/x) == {a: 6/x}

