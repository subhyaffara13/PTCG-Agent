
def test_issue_3506():
    e = (x + sin(3*x))**(-2)*(x*(x + sin(3*x)) - (x + sin(3*x))*sin(2*x))
    assert e.nseries(x, n=7) == \
        Rational(-1, 4) + 5*x**2/96 + 91*x**4/768 + 11117*x**6/129024 + O(x**7)

