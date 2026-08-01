
def test_issue_22836():
    assert O(2**x + factorial(x), (x, oo)) == O(factorial(x), (x, oo))
    assert O(2**x + factorial(x) + x**x, (x, oo)) == O(exp(x*log(x)), (x, oo))
    assert O(x + factorial(x), (x, oo)) == O(factorial(x), (x, oo))

