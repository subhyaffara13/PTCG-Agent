
def test_issue_26040():
    assert limit(besseli(0, x + 1)/besseli(0, x), x, oo) == S.Exp1

