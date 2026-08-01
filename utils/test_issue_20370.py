
def test_issue_20370():
    a = symbols('a', positive=True)
    assert integrate((1 + a * cos(x))**-1, (x, 0, 2 * pi)) == (2 * pi / sqrt(1 - a**2))

