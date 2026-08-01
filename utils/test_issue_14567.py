
def test_issue_14567():
    assert factorial(Sum(-1, (x, 0, 0))) + y  # doesn't raise an error

