
def test_issue_9116():
    n = Symbol('n', positive=True, integer=True)
    assert log(n).is_nonnegative is True

