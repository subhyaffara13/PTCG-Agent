
def test_issue_4052():
    f = S.Half*asin(x) + x*sqrt(1 - x**2)/2

    assert integrate(cos(asin(x)), x) == f
    assert integrate(sin(acos(x)), x) == f

