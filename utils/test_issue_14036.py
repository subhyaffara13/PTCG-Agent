
def test_issue_14036():
    a, n = symbols('a n')
    assert product(1 - a**2 / (n*pi)**2, [n, 1, oo]) != 0

