
def test_issue_4171():
    assert summation(factorial(2*k + 1)/factorial(2*k), (k, 0, oo)) is oo
    assert summation(2*k + 1, (k, 0, oo)) is oo

