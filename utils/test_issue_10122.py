
def test_issue_10122():
    assert solve(abs(x) + abs(x - 1) - 1 > 0, x
        ) == Or(And(-oo < x, x < S.Zero), And(S.One < x, x < oo))

