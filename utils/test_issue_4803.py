
def test_issue_4803():
    x_max = Symbol("x_max")
    assert integrate(y/pi*exp(-(x_max - x)/cos(a)), x) == \
        y*exp((x - x_max)/cos(a))*cos(a)/pi

