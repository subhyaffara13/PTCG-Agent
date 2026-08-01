
def test_issue_10680():
    assert isinstance(integrate(x**log(x**log(x**log(x))),x), Integral)

