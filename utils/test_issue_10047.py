
def test_issue_10047():
    # issue 10047: this must remain an inequality, not True, since if x
    # is not real the inequality is invalid
    # assert solve(sin(x) < 2) == (x <= oo)

    # with PR 16956, (x <= oo) autoevaluates when x is extended_real
    # which is assumed in the current implementation of inequality solvers
    assert solve(sin(x) < 2) == True
    assert solveset(sin(x) < 2, domain=S.Reals) == S.Reals

