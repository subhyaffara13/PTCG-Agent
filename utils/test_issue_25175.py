
def test_issue_25175():
    x = Symbol('x')
    g1 = 2*acosh(1 + 2*x/3) - acosh(S(5)/3 - S(8)/3/(x + 4))
    g2 = 2*log(sqrt((x + 4)/3)*(sqrt(x + 3)+sqrt(x))**2/(2*sqrt(x + 3) + sqrt(x)))
    assert (g1 - g2).series(x) == O(x**6)

