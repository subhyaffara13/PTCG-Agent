
def test_issue_3644():
    assert gruntz(((x**7 + x + 1)/(2**x + x**2))**(-1/x), x, oo) == 2

