
def test_issue_9308():
    assert limit_seq(subfactorial(n)/factorial(n), n) == exp(-1)

