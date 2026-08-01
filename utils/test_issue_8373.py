
def test_issue_8373():
    x = Symbol('x', real=True)
    assert simplify(Or(x < 1, x >= 1)) == S.true


def test_issue_8373():
    x = symbols('x', real=True)
    assert Or(x < 1, x > -1).simplify() == S.true
    assert Or(x < 1, x >= 1).simplify() == S.true
    assert And(x < 1, x >= 1).simplify() == S.false
    assert Or(x <= 1, x >= 1).simplify() == S.true

