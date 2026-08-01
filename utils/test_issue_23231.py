
def test_issue_23231():
    f = (2**x - 2**(-x))/(2**x + 2**(-x))
    assert limit(f, x, -oo) == -1


def test_issue_23231():
    # This test checks Order for expressions having
    # arguments containing variables in exponents/powers.
    assert O(x**x + 2**x, (x, oo)) == O(exp(x*log(x)), (x, oo))
    assert O(x**x + x**2, (x, oo)) == O(exp(x*log(x)), (x, oo))
    assert O(x**x + 1/x**2, (x, oo)) == O(exp(x*log(x)), (x, oo))
    assert O(2**x + 3**x , (x, oo)) == O(exp(x*log(3)), (x, oo))

