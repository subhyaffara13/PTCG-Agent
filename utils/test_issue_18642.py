
def test_issue_18642():
    i = Symbol("i", integer=True)
    n = Symbol("n", integer=True)
    expr = And(Eq(i, 2 * n), Le(i, 2*n -1))
    assert simplify(expr) == S.false

