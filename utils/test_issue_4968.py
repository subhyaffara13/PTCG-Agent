
def test_issue_4968():
    assert integrate(sin(log(x**2))) == x*sin(log(x**2))/5 - 2*x*cos(log(x**2))/5

