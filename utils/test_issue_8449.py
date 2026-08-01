
def test_issue_8449():
    p = Symbol('p', nonnegative=True)
    assert Lt(-oo, p)
    assert Ge(-oo, p) is S.false
    assert Gt(oo, -p)
    assert Le(oo, -p) is S.false

