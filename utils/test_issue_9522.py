
def test_issue_9522():
    expr1 = Eq(1/(x**2 - 4) + x, 1/(x**2 - 4) + 2)
    expr2 = Eq(1/x + x, 1/x)

    assert solveset(expr1, x, S.Reals) is S.EmptySet
    assert solveset(expr2, x, S.Reals) is S.EmptySet

