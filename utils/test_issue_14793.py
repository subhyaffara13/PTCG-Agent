
def test_issue_14793():
    expr = ((x + S(1)/2) * log(x) - x + log(2*pi)/2 - \
        log(factorial(x)) + S(1)/(12*x))*x**3
    assert limit(expr, x, oo) == S(1)/360

