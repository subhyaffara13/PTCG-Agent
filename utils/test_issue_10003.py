
def test_issue_10003():
    X = Exponential('x', 3)
    G = Gamma('g', 1, 2)
    assert P(X < -1) is S.Zero
    assert P(G < -1) is S.Zero

