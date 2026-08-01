
def test_issue_7027():
    for wrt in (cos(x), re(x), Derivative(cos(x), x)):
        raises(ValueError, lambda: diff(f(x), wrt))

