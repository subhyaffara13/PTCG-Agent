
def test_issue_11134():
    alpha, n, p = 0.95, 10, 0
    assert_equal(binom.interval(confidence=alpha, n=n, p=p), (0, 0))

