
def test_issue_7179():
    assert upretty(Not(Equivalent(x, y))) == 'x ⇎ y'
    assert upretty(Not(Implies(x, y))) == 'x ↛ y'

