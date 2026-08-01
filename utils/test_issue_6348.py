
def test_issue_6348():
    assert integrate(exp(I*x)/(1 + x**2), (x, -oo, oo)).simplify().rewrite(exp) \
        == pi*exp(-1)

