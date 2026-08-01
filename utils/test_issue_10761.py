
def test_issue_10761():
    assert series(1/(x**-2 + x**-3), x, 0) == x**3 - x**4 + x**5 + O(x**6)

