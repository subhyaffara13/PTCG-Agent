
def test_issue_3103():
    e = -2*sqrt(x) - y/sqrt(x)/2
    assert str(e) not in ["(-2)*x**1/2(-1/2)*x**(-1/2)*y",
            "-2*x**1/2(-1/2)*x**(-1/2)*y", "-2*x**1/2-1/2*x**-1/2*w"]
    assert str(e) == "-2*sqrt(x) - y/(2*sqrt(x))"

