
def test_issue_4441():
    a, b = symbols('a,b')
    f = 1/(1 + a*x)
    assert f.series(x, 0, 5) == 1 - a*x + a**2*x**2 - a**3*x**3 + \
        a**4*x**4 + O(x**5)
    f = 1/(1 + (a + b)*x)
    assert f.series(x, 0, 3) == 1 + x*(-a - b)\
        + x**2*(a + b)**2 + O(x**3)

