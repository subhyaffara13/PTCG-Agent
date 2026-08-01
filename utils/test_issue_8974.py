
def test_issue_8974():
    assert isolve(-oo < x, x) == And(-oo < x, x < oo)
    assert isolve(oo > x, x) == And(-oo < x, x < oo)

