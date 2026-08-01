
def test_issue_10382():
    assert limit(fibonacci(n + 1)/fibonacci(n), n, oo) == GoldenRatio


def test_issue_10382():
    n = Symbol('n', integer=True)
    assert limit_seq(fibonacci(n+1)/fibonacci(n), n).together() == S.GoldenRatio

