
def test_issue_10488():
    a,b,c,x = symbols('a b c x', positive=True)
    assert integrate(x/(a*x+b),x) == x/a - b*log(a*x + b)/a**2

