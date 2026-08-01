
def test_issue_12996():
    # foo=True imitates the sort of arguments that Derivative can get
    # from Integral when it passes doit to the expression
    assert Derivative(im(x), x).doit(foo=True) == Derivative(im(x), x)

