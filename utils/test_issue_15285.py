
def test_issue_15285():
    y = 1/x - 1
    f = 4*y*exp(-2*y)/x**2
    assert integrate(f, [x, 0, 1]) == 1

