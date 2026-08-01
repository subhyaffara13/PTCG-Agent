
def test_issue_9549():
    y = (x**2 + x + 1) / (x**3 + x**2)
    assert series(y, x, oo) == x**(-5) - 1/x**4 + x**(-3) + 1/x + O(x**(-6), (x, oo))

