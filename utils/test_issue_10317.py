
def test_issue_10317():
    alpha, n, p = 0.9, 10, 1
    assert_equal(nbinom.interval(confidence=alpha, n=n, p=p), (0, 0))

