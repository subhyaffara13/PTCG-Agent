
def test_issue_3501():
    a = Symbol("a")
    e = x**(-2)*(x*sin(a + x) - x*sin(a))
    assert e.nseries(x, n=6) == cos(a) - sin(a)*x/2 - cos(a)*x**2/6 + \
        x**3*sin(a)/24 + x**4*cos(a)/120 - x**5*sin(a)/720 + O(x**6)
    e = x**(-2)*(x*cos(a + x) - x*cos(a))
    assert e.nseries(x, n=6) == -sin(a) - cos(a)*x/2 + sin(a)*x**2/6 + \
        cos(a)*x**3/24 - x**4*sin(a)/120 - x**5*cos(a)/720 + O(x**6)

