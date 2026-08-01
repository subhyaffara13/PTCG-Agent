
def test_issue_13462():
    assert limit(n**2*(2*n*(-(1 - 1/(2*n))**x + 1) - x - (-x**2/4 + x/4)/n), n, oo) == x**3/24 - x**2/8 + x/12

