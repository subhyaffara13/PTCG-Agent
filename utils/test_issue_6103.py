
def test_issue_6103():
    x = Symbol('x')
    a = Wild('a')
    assert (-I*x*oo).match(I*a*oo) == {a: -x}

