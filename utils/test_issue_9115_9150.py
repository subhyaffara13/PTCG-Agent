
def test_issue_9115_9150():
    n = Dummy('n', integer=True, nonnegative=True)
    assert (factorial(n) >= 1) == True
    assert (factorial(n) < 1) == False

    assert factorial(n + 1).is_even is None
    assert factorial(n + 2).is_even is True
    assert factorial(n + 2) >= 2

