
def test_issue_8462():
    assert limit(binomial(n, n/2), n, oo) == oo
    assert limit(binomial(n, n/2) * 3 ** (-n), n, oo) == 0

