
def test_issue_19868():
    assert limit_seq(1/gamma(n + S.One/2), n) == 0

