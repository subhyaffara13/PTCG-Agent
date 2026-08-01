
def test_issue_9462():
    assert manualintegrate(sin(2*x)*exp(x), x) == exp(x)*sin(2*x)/5 - 2*exp(x)*cos(2*x)/5
    assert not integral_steps(sin(2*x)*exp(x), x).contains_dont_know()
    assert manualintegrate((x - 3) / (x**2 - 2*x + 2)**2, x) == \
                           Integral(x/(x**4 - 4*x**3 + 8*x**2 - 8*x + 4), x) \
                           - 3*Integral(1/(x**4 - 4*x**3 + 8*x**2 - 8*x + 4), x)

