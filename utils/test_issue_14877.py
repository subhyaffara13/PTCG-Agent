
def test_issue_14877():
    f = exp(1 - exp(x**2)*x + 2*x**2)*(2*x**3 + x)/(1 - exp(x**2)*x)**2
    assert integrate(f, x) == \
        -exp(2*x**2 - x*exp(x**2) + 1)/(x*exp(3*x**2) - exp(2*x**2))

