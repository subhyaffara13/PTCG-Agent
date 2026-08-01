
def test_issue_17751():
    a, b, c, x = symbols('a b c x', positive=True)
    assert limit((a + 1)*x - sqrt((a + 1)**2*x**2 + b*x + c), x, oo) == -b/(2*a + 2)

