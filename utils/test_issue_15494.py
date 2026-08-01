
def test_issue_15494():
    s = symbols('s', positive=True)

    integrand = (exp(s/2) - 2*exp(1.6*s) + exp(s))*exp(s)
    solution = integrate(integrand, s)
    assert solution != S.NaN
    # Not sure how to test this properly as it is a symbolic expression with floats
    # assert str(solution) == '0.666666666666667*exp(1.5*s) + 0.5*exp(2.0*s) - 0.769230769230769*exp(2.6*s)'
    # Maybe
    assert abs(solution.subs(s, 1) - (-3.67440080236188)) <= 1e-8

    integrand = (exp(s/2) - 2*exp(S(8)/5*s) + exp(s))*exp(s)
    assert integrate(integrand, s) == -10*exp(13*s/5)/13 + 2*exp(3*s/2)/3 + exp(2*s)/2

