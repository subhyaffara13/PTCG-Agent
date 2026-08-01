
def test_issue_4884():
    assert integrate(sqrt(x)*(1 + x)) == \
        Piecewise(
            (2*sqrt(x)*(x + 1)**2/5 - 2*sqrt(x)*(x + 1)/15 - 4*sqrt(x)/15,
            Abs(x + 1) > 1),
            (2*I*sqrt(-x)*(x + 1)**2/5 - 2*I*sqrt(-x)*(x + 1)/15 -
            4*I*sqrt(-x)/15, True))
    assert integrate(x**x*(1 + log(x))) == x**x

