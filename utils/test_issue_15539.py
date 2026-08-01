
def test_issue_15539():
    assert O(1/x**2 + 1/x**4, (x, -oo)) == O(1/x**2, (x, -oo))
    assert O(1/x**4 + exp(x), (x, -oo)) == O(1/x**4, (x, -oo))
    assert O(1/x**4 + exp(-x), (x, -oo)) == O(exp(-x), (x, -oo))
    assert O(1/x, (x, oo)).subs(x, -x) == O(-1/x, (x, -oo))


def test_issue_15539():
    assert series(atan(x), x, -oo) == (-1/(5*x**5) + 1/(3*x**3) - 1/x - pi/2
        + O(x**(-6), (x, -oo)))
    assert series(atan(x), x, oo) == (-1/(5*x**5) + 1/(3*x**3) - 1/x + pi/2
        + O(x**(-6), (x, oo)))

