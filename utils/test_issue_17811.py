
def test_issue_17811():
    a = Function('a')
    assert sympify('a(x)*5', evaluate=False) == Mul(a(x), 5, evaluate=False)

