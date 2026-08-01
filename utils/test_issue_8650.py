
def test_issue_8650():
    n = Symbol('n', integer=True, nonnegative=True)
    assert (n**n).is_positive is True
    x = 5*n + 5
    assert (x**(5*(n + 1))).is_positive is True

