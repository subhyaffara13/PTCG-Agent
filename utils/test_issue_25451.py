
def test_issue_25451():
    x = Or(And(a, c), Eq(a, b))
    assert isinstance(x, Or)
    assert set(x.args) == {And(a, c), Eq(a, b)}

