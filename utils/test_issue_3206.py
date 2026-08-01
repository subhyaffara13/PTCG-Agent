
def test_issue_3206():
    x = Symbol('x')
    assert Abs(Abs(x)) == Abs(x)

