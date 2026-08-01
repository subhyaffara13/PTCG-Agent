
def test_issue_16735():
    assert limit_seq(5**n/factorial(n), n) == 0


def test_issue_16735():
    assert Sum(5**n/gamma(n+1), (n, 1, oo)).is_convergent() is S.true

