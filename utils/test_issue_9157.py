
def test_issue_9157():
    n = Symbol('n', integer=True, positive=True)
    assert atan(n - 1).is_nonnegative is True

