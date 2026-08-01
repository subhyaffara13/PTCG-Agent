
def test_issue_21530():
    assert limit(sinh(n + 1)/sinh(n), n, oo) == E

