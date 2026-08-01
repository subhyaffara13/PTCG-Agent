
def test_issue_14779():
    x = symbols('x', real=True)
    assert solve(sqrt(x**4 - 130*x**2 + 1089) + sqrt(x**4 - 130*x**2
                 + 3969) - 96*Abs(x)/x,x) == [sqrt(130)]

