
def test_issue_10268():
    assert solve(log(x) < 1000) == And(S.Zero < x, x < exp(1000))

