
def test_issue_4035():
    x = Symbol('x')
    assert Abs(x).expand(trig=True) == Abs(x)
    assert sign(x).expand(trig=True) == sign(x)
    assert arg(x).expand(trig=True) == arg(x)

