
def test_issue_5249():
    assert ratint(
        1/(x**2 + a**2), x) == (-I*log(-I*a + x)/2 + I*log(I*a + x)/2)/a

