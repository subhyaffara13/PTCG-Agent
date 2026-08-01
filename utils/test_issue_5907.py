
def test_issue_5907():
    a = symbols('a', nonzero=True)
    assert integrate(1/(x**2 + a**2)**2, x) == \
         x/(2*a**4 + 2*a**2*x**2) + atan(x/a)/(2*a**3)

