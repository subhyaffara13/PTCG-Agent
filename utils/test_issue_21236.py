
def test_issue_21236():
    x, z = symbols("x z")
    y = symbols('y', rational=True)
    assert solveset(x**y - z, x, S.Reals) == ConditionSet(x, Eq(x**y - z, 0), S.Reals)
    e1, e2 = symbols('e1 e2', even=True)
    y = e1/e2  # don't know if num or den will be odd and the other even
    assert solveset(x**y - z, x, S.Reals) == ConditionSet(x, Eq(x**y - z, 0), S.Reals)

