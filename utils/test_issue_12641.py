
def test_issue_12641():
    assert manualintegrate(sin(2*x), x) == -cos(2*x)/2
    assert manualintegrate(cos(x)*sin(2*x), x) == -2*cos(x)**3/3
    assert manualintegrate((sin(2*x)*cos(x))/(1 + cos(x)), x) == \
        -2*log(cos(x) + 1) - cos(x)**2 + 2*cos(x)

