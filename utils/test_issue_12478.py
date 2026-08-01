
def test_issue_12478():
    eq = sqrt(x - 2) + 2
    soln = solveset_real(eq, x)
    assert soln is S.EmptySet
    assert solveset(eq < 0, x, S.Reals) is S.EmptySet
    assert solveset(eq > 0, x, S.Reals) == Interval(2, oo)

