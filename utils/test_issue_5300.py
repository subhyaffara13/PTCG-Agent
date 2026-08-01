
def test_issue_5300():
    x = Symbol('x', commutative=False)
    assert x*sqrt(2)/sqrt(6) == x*sqrt(3)/3

